# Copyright (c) 2016-2019 Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import json
from functools import lru_cache
import os
import re
from tempfile import NamedTemporaryFile
import typing as tp

from packaging.version import parse
from subprocess import Popen, PIPE

from notebook.utils import url_path_join, url2path
from tornado import gen, httpclient, httputil, ioloop, web
from traitlets.config.configurable import LoggingConfigurable

ROOT_ENV_NAME = "base"


def normalize_pkg_info(
    s: tp.Dict[str, tp.Any]
) -> tp.Dict[str, tp.Union[str, tp.List[str]]]:
    return {
        "build_number": s.get("build_number"),
        "build_string": s.get("build_string", s.get("build")),
        "channel": s.get("channel"),
        "name": s.get("name"),
        "platform": s.get("platform"),
        "version": s.get("version"),
        "summary": s.get("summary", ""),
        "home": s.get("home", ""),
        "keywords": s.get("keywords", []),
        "tags": s.get("tags", []),
    }


MAX_LOG_OUTPUT = 6000  # type: int

CONDA_EXE = os.environ.get("CONDA_EXE", "conda")  # type: str

# try to match lines of json
JSONISH_RE = r'(^\s*["\{\}\[\],\d])|(["\}\}\[\],\d]\s*$)'  # type: str

# these are the types of environments that can be created
package_map = {
    "python2": "python=2 ipykernel",
    "python3": "python=3 ipykernel",
    "r": "r-base r-essentials",
}  # type: tp.Dict[str, str]


class EnvManager(LoggingConfigurable):
    def _call_subprocess(self, cmdline: tp.List[str]) -> tp.Tuple[int, bytes, bytes]:
        process = Popen(cmdline, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        return (process.returncode, output, error)

    @gen.coroutine
    def _execute(self, cmd: str, *args) -> tp.Tuple[int, str]:
        cmdline = [cmd]
        cmdline.extend(args)

        self.log.debug("[jupyter_conda] command: {!s}".format(" ".join(cmdline)))

        current_loop = ioloop.IOLoop.current()
        returncode, output, error = yield current_loop.run_in_executor(
            None, self._call_subprocess, cmdline
        )

        if returncode == 0:
            output = output.decode("utf-8")
        else:
            self.log.debug("[jupyter_conda] exit code: {!s}".format(returncode))
            output = error.decode("utf-8") + output.decode("utf-8")

        self.log.debug("[jupyter_conda] output: {!s}".format(output[:MAX_LOG_OUTPUT]))

        if len(output) > MAX_LOG_OUTPUT:
            self.log.debug("[jupyter_conda] ...")

        return returncode, output

    @lru_cache(maxsize=4)
    @gen.coroutine
    def list_envs(self) -> tp.Dict[str, tp.List[tp.Dict[str, tp.Union[str, bool]]]]:
        """List all environments that conda knows about"""
        ans = yield self._execute(CONDA_EXE, "info", "--json")
        rcode, output = ans
        info = self.clean_conda_json(output)
        if rcode > 0:
            return info

        default_env = info["default_prefix"]

        root_env = {
            "name": ROOT_ENV_NAME,
            "dir": info["root_prefix"],
            "is_default": info["root_prefix"] == default_env,
        }

        def get_info(env):
            base_dir = os.path.dirname(env)
            if base_dir not in info["envs_dirs"]:
                return None

            return {
                "name": os.path.basename(env),
                "dir": env,
                "is_default": env == default_env,
            }

        envs_list = [root_env]
        for env in info["envs"]:
            env_info = get_info(env)
            if env_info is not None:
                envs_list.append(env_info)

        return {"environments": envs_list}

    @gen.coroutine
    def delete_env(self, env: str) -> tp.Dict[str, str]:
        ans = yield self._execute(
            CONDA_EXE, "env", "remove", "-y", "-q", "--json", "-n", env
        )

        # Force updating environment listing
        self.list_envs.cache_clear()

        rcode, output = ans
        if rcode > 0:
            return {"error": output}
        return output

    def clean_conda_json(self, output: str) -> tp.Dict[str, tp.Any]:
        lines = output.splitlines()

        try:
            return json.loads("\n".join(lines))
        except (ValueError, json.JSONDecodeError) as err:
            self.log.warn("[jupyter_conda] JSON parse fail:\n{!s}".format(err))

        # try to remove bad lines
        lines = [line for line in lines if re.match(JSONISH_RE, line)]

        try:
            return json.loads("\n".join(lines))
        except (ValueError, json.JSONDecodeError) as err:
            self.log.error("[jupyter_conda] JSON clean/parse fail:\n{!s}".format(err))

        return {"error": True}

    @gen.coroutine
    def export_env(self, env: str) -> tp.Dict[str, str]:
        ans = yield self._execute(CONDA_EXE, "env", "export", "-n", env)
        rcode, output = ans
        if rcode > 0:
            return {"error": output}
        return output

    @gen.coroutine
    def clone_env(self, env: str, name: str) -> tp.Dict[str, str]:
        ans = yield self._execute(
            CONDA_EXE, "create", "-y", "-q", "--json", "-n", name, "--clone", env
        )

        # Force updating environment listing
        self.list_envs.cache_clear()

        rcode, output = ans
        if rcode > 0:
            return {"error": output}
        return output

    @gen.coroutine
    def create_env(self, env: str, type: str) -> tp.Dict[str, str]:
        packages = package_map.get(type, type)
        ans = yield self._execute(
            CONDA_EXE, "create", "-y", "-q", "--json", "-n", env, *packages.split()
        )

        # Force updating environment listing
        self.list_envs.cache_clear()
        
        rcode, output = ans
        if rcode > 0:
            return {"error": output}
        return output

    @gen.coroutine
    def import_env(self, env: str, file_content: str, file_name: str="environment.txt") -> tp.Dict[str, str]:
        with NamedTemporaryFile(mode="w", delete=False, suffix=file_name) as f:
            name = f.name
            f.write(file_content)

        ans = yield self._execute(
            CONDA_EXE, "env", "create", "-q", "--json", "-n", env, "--file", name
        )
        # Remove temporary file
        os.unlink(name)

        # Force updating environment listing
        self.list_envs.cache_clear()

        rcode, output = ans
        if rcode > 0:
            return {"error": output}
        return output

    @lru_cache(maxsize=64)
    @gen.coroutine
    def env_channels(self, env: str) -> tp.Dict[str, tp.Dict[str, tp.List[str]]]:
        if env != ROOT_ENV_NAME and "CONDA_PREFIX" in os.environ:
            old_prefix = os.environ["CONDA_PREFIX"]
            envs = yield self.list_envs()
            envs = envs["environments"]
            env_dir = None
            for env_i in envs:
                if env_i["name"] == env:
                    env_dir = env_i["dir"]
                    break

            os.environ["CONDA_PREFIX"] = env_dir
            ans = yield self._execute(CONDA_EXE, "config", "--show", "--json")
            _, output = ans
            info = self.clean_conda_json(output)
            os.environ["CONDA_PREFIX"] = old_prefix
        else:
            ans = yield self._execute(CONDA_EXE, "config", "--show", "--json")
            _, output = ans
            info = self.clean_conda_json(output)

        if "error" in info:
            return info

        deployed_channels = {}

        def get_uri(spec):
            location = "/".join((spec["location"], spec["name"]))
            if spec["scheme"] == "file" and location[0] != "/":
                location = "/" + location
            return spec["scheme"] + "://" + location

        for channel in info["channels"]:
            if channel in info["custom_multichannels"]:
                deployed_channels[channel] = [
                    get_uri(entry) for entry in info["custom_multichannels"][channel]
                ]
            elif os.path.sep not in channel:
                spec = info["channel_alias"]
                spec["name"] = channel
                deployed_channels[channel] = [get_uri(spec)]
            else:
                deployed_channels[channel] = ["file:///" + channel]

        self.log.debug("[jupyter_conda] {} channels: {}".format(env, deployed_channels))
        return {"channels": deployed_channels}

    @gen.coroutine
    def env_packages(self, env: str) -> tp.Dict[str, tp.List[str]]:
        ans = yield self._execute(CONDA_EXE, "list", "--no-pip", "--json", "-n", env)
        _, output = ans
        data = self.clean_conda_json(output)

        # Data structure
        #   List of dictionary. Example:
        # {
        #     "base_url": null,
        #     "build_number": 0,
        #     "build_string": "py36_0",
        #     "channel": "defaults",
        #     "dist_name": "anaconda-client-1.6.14-py36_0",
        #     "name": "anaconda-client",
        #     "platform": null,
        #     "version": "1.6.14"
        # }

        if "error" in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        return {"packages": [normalize_pkg_info(package) for package in data]}

    @lru_cache(maxsize=64)
    @gen.coroutine
    def list_available(self) -> tp.List[tp.Dict[str, str]]:
        ans = yield self._execute(CONDA_EXE, "search", "--json")
        _, output = ans
        data = self.clean_conda_json(output)

        if "error" in data:
            # we didn't get back a list of packages, we got a
            # dictionary with error info
            return data

        packages = []

        # Data structure
        #  Dictionary with package name key and value is a list of dictionary. Example:
        #  {
        #   "arch": "x86_64",
        #   "build": "np17py33_0",
        #   "build_number": 0,
        #   "channel": "https://repo.anaconda.com/pkgs/free/win-64",
        #   "constrains": [],
        #   "date": "2013-02-20",
        #   "depends": [
        #     "numpy 1.7*",
        #     "python 3.3*"
        #   ],
        #   "fn": "astropy-0.2-np17py33_0.tar.bz2",
        #   "license": "BSD",
        #   "md5": "3522090a8922faebac78558fbde9b492",
        #   "name": "astropy",
        #   "platform": "win32",
        #   "size": 3352442,
        #   "subdir": "win-64",
        #   "url": "https://repo.anaconda.com/pkgs/free/win-64/astropy-0.2-np17py33_0.tar.bz2",
        #   "version": "0.2"
        # }

        # List all available version for packages
        for entries in data.values():
            pkg_entry = None
            versions = list()
            max_build_numbers = list()
            max_build_strings = list()

            for entry in entries:
                entry = normalize_pkg_info(entry)
                if pkg_entry is None:
                    pkg_entry = entry

                version = parse(entry.get("version", ""))

                if version not in versions:
                    versions.append(version)
                    max_build_numbers.append(entry.get("build_number", 0))
                    max_build_strings.append(entry.get("build_string", ""))
                else:
                    version_idx = versions.index(version)
                    build_number = entry.get("build_number", 0)
                    if build_number > max_build_numbers[version_idx]:
                        max_build_numbers[version_idx] = build_number
                        max_build_strings[version_idx] = entry.get("build_string", "")

            sorted_versions_idx = sorted(range(len(versions)), key=versions.__getitem__)

            pkg_entry["version"] = [str(versions[i]) for i in sorted_versions_idx]
            pkg_entry["build_number"] = [
                max_build_numbers[i] for i in sorted_versions_idx
            ]
            pkg_entry["build_string"] = [
                max_build_strings[i] for i in sorted_versions_idx
            ]

            packages.append(pkg_entry)

        # Get channel short names
        channels = yield self.env_channels(ROOT_ENV_NAME)
        channels = channels["channels"]
        tr_channels = {}
        for short_name, channel in channels.items():
            tr_channels.update({uri: short_name for uri in channel})

        # # Get top channel URI to request channeldata.json
        # top_channels = set()
        # for uri in tr_channels:
        #     channel, arch = os.path.split(uri)
        #     if arch in PLATFORMS:
        #         top_channels.add(channel)
        #     else:
        #         top_channels.add(uri)

        # Request channeldata.json
        pkg_info = {}
        client = httpclient.AsyncHTTPClient(force_instance=True)
        for channel in tr_channels:
            url = httputil.urlparse(channel)
            if url.scheme == "file":
                path = (
                    "".join(("//", url.netloc, url.path))
                    if url.netloc
                    else url.path.lstrip("/")
                )
                path = path.rstrip("/") + "/channeldata.json"
                try:  # Skip if file is not accessible
                    with open(path) as f:
                        channeldata = json.load(f)
                except OSError as err:
                    self.log.info("[jupyter_conda] Error: {}".format(str(err)))
                else:
                    pkg_info.update(channeldata["packages"])
            else:
                try:  # Skip if file is not accessible
                    response = yield client.fetch(
                        httpclient.HTTPRequest(
                            url_path_join(channel, "channeldata.json"),
                            headers={"Content-Type": "application/json"},
                        )
                    )
                except (httpclient.HTTPClientError, ConnectionError) as e:
                    self.log.info(
                        "[jupyter_conda] Error getting {}/channeldata.json: {}".format(
                            channel, str(e)
                        )
                    )
                else:
                    channeldata = response.body.decode("utf-8")
                    pkg_info.update(json.loads(channeldata)["packages"])

        # Example structure channeldata['packages'] for channeldata_version == 1
        # "tmpc0d7d950": {
        #     "activate.d": false,
        #     "binary_prefix": false,
        #     "deactivate.d": false,
        #     "identifiers": [],
        #     "keywords": [
        #         "['package', 'tmpc0d7d950']"
        #     ],
        #     "license": "MIT",
        #     "post_link": false,
        #     "pre_link": false,
        #     "pre_unlink": false,
        #     "reference_package": "win-64/tmpc0d7d950-0.1.0.dev1-py36_0.tar.bz2",
        #     "run_exports": {},
        #     "subdirs": [
        #         "win-64"
        #     ],
        #     "summary": "Dummy package",
        #     "tags": [],
        #     "text_prefix": false,
        #     "version": "0.1.0.dev1"
        # }

        # Update channel and add some info
        for package in packages:
            name = package["name"]
            if name in pkg_info:
                package["summary"] = pkg_info[name].get("summary", "")
                package["home"] = pkg_info[name].get("home", "")
                package["keywords"] = pkg_info[name].get("keywords", [])
                package["tags"] = pkg_info[name].get("tags", [])

            # Convert to short channel names
            channel, _ = os.path.split(package["channel"])
            if channel in tr_channels:
                package["channel"] = tr_channels[channel]

        return sorted(packages, key=lambda entry: entry.get("name"))

    @gen.coroutine
    def check_update(
        self, env: str, packages: tp.List[str]
    ) -> tp.Dict[str, tp.List[tp.Dict[str, str]]]:
        ans = yield self._execute(
            CONDA_EXE, "update", "--dry-run", "-q", "--json", "-n", env, *packages
        )
        _, output = ans
        data = self.clean_conda_json(output)

        # Data structure in LINK
        #   List of dictionary. Example:
        # {
        #     "base_url": null,
        #     "build_number": 0,
        #     "build_string": "mkl",
        #     "channel": "defaults",
        #     "dist_name": "blas-1.0-mkl",
        #     "name": "blas",
        #     "platform": null,
        #     "version": "1.0"
        # }

        if "error" in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data
        elif "actions" in data:
            links = data["actions"].get("LINK", [])
            package_versions = [link for link in links]
            return {
                "updates": [
                    normalize_pkg_info(pkg_version) for pkg_version in package_versions
                ]
            }
        else:
            # no action plan returned means everything is already up to date
            return {"updates": []}

    @gen.coroutine
    def install_packages(self, env: str, packages: tp.List[str]) -> tp.Dict[str, str]:
        ans = yield self._execute(
            CONDA_EXE, "install", "-y", "-q", "--json", "-n", env, *packages
        )
        _, output = ans
        return self.clean_conda_json(output)

    @gen.coroutine
    def develop_packages(
        self, env: str, packages: tp.List[str]
    ) -> tp.Dict[str, tp.List[tp.Dict[str, str]]]:
        envs = yield self.list_envs()
        if "error" in envs:
            return envs

        env_rootpath = list(filter(lambda e: e["name"] == env, envs["environments"]))
        result = []
        if env_rootpath:
            python_cmd = os.path.join(env_rootpath[0]["dir"], "python")
            for path in packages:
                realpath = os.path.realpath(os.path.expanduser(path))
                ans = yield self._execute(
                    python_cmd,
                    "-m",
                    "pip",
                    "install",
                    "--progress-bar",
                    "off",
                    "-e",
                    realpath,
                )
                rcode, output = ans
                if rcode > 0:
                    return {"error": output}
                feedback = {"path": path, "output": output}
                result.append(feedback)
        return {"packages": result}

    @gen.coroutine
    def update_packages(self, env: str, packages: tp.List[str]) -> tp.Dict[str, str]:
        ans = yield self._execute(
            CONDA_EXE, "update", "-y", "-q", "--json", "-n", env, *packages
        )
        _, output = ans
        return self.clean_conda_json(output)

    @gen.coroutine
    def remove_packages(self, env: str, packages: tp.List[str]) -> tp.Dict[str, str]:
        ans = yield self._execute(
            CONDA_EXE, "remove", "-y", "-q", "--json", "-n", env, *packages
        )
        _, output = ans
        return self.clean_conda_json(output)

    @gen.coroutine
    def package_search(self, q: str) -> tp.Dict[str, str]:
        # this method is slow
        ans = yield self._execute(CONDA_EXE, "search", "--json", q)
        _, output = ans
        data = self.clean_conda_json(output)

        if "error" in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        packages = []

        for entries in data.values():
            max_version = None
            max_version_entry = None

            for entry in entries:
                version = parse(entry.get("version", ""))

                if max_version is None or version > max_version:
                    max_version = version
                    max_version_entry = entry

            packages.append(max_version_entry)

        return {"packages": sorted(packages, key=lambda entry: entry.get("name"))}
