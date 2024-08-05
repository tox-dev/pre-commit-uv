"""Package root."""

from __future__ import annotations

import logging
import os
from functools import cache
from importlib.metadata import version as _metadata_version
from typing import TYPE_CHECKING, cast

from pre_commit import lang_base, main
from pre_commit.languages import python
from pre_commit.languages.python import in_env, norm_version
from pre_commit.util import CalledProcessError, cmd_output, cmd_output_b
from uv import find_uv_bin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pre_commit.prefix import Prefix


__version__ = _metadata_version("pre-commit-uv")
_uv_version = _metadata_version("uv")
_original_main = main.main


def _patch() -> None:
    if os.environ.get("DISABLE_PRE_COMMIT_UV_PATCH") is None:
        main.main = _new_main


def _new_main(argv: Sequence[str] | None = None) -> int:
    python.install_environment = _install_environment
    python._version_info = _version_info  # noqa: SLF001
    return cast(int, _original_main(argv))


def _install_environment(
    prefix: Prefix,
    version: str,
    additional_dependencies: Sequence[str],
) -> None:
    logging.getLogger("pre_commit").info("Using pre-commit with uv %s via pre-commit-uv %s", _uv_version, __version__)
    uv = find_uv_bin()

    venv_cmd = [uv, "venv", lang_base.environment_dir(prefix, python.ENVIRONMENT_DIR, version)]
    py = norm_version(version)
    if py is not None:
        venv_cmd.extend(("-p", py))
    cmd_output_b(*venv_cmd, cwd="/")

    with in_env(prefix, version):
        lang_base.setup_cmd(prefix, (uv, "pip", "install", ".", *additional_dependencies))


@cache
def _version_info(exe: str) -> str:
    prog = 'import sys;print(".".join(str(p) for p in sys.version_info[0:3]))'
    try:
        return cast(str, cmd_output(exe, "-S", "-c", prog)[1].strip())
    except CalledProcessError:
        return f"<<error retrieving version from {exe}>>"


__all__ = [
    "__version__",
]
