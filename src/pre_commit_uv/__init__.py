"""Package root."""

from __future__ import annotations

# only import built-ins at top level to avoid interpreter startup overhead
import os
import sys

_original_main = None


def _patch() -> None:
    global _original_main
    if _original_main is not None:  # already patched, nothing more to do
        return
    calling_pre_commit = "FORCE_PRE_COMMIT_UV_PATCH" in os.environ
    if not calling_pre_commit and sys.argv and sys.argv[0]:  # must have arguments
        calling = sys.argv[1] if sys.argv[0] == sys.executable and len(sys.argv) >= 1 else sys.argv[0]
        if os.path.split(calling)[1] == f"pre-commit{'.exe' if sys.platform == 'win32' else ''}":
            calling_pre_commit = True

    if calling_pre_commit and os.environ.get("DISABLE_PRE_COMMIT_UV_PATCH") is None:
        from pre_commit import main  # noqa: PLC0415

        _original_main, main.main = main.main, _new_main
        if "--version" in sys.argv:
            from importlib.metadata import version as _metadata_version  # noqa: PLC0415

            from pre_commit import constants  # noqa: PLC0415

            constants.VERSION = (
                f"{constants.VERSION} ("
                f"pre-commit-uv={_metadata_version('pre-commit-uv')}, "
                f"uv={_metadata_version('uv')}"
                f")"
            )


def _new_main(argv: list[str] | None = None) -> int:
    # imports applied locally to avoid patching import overhead cost
    from functools import cache  # noqa: PLC0415
    from typing import TYPE_CHECKING, cast  # noqa: PLC0415

    from pre_commit.languages import python  # noqa: PLC0415

    if TYPE_CHECKING:
        from collections.abc import Sequence  # noqa: PLC0415

        from pre_commit.prefix import Prefix  # noqa: PLC0415

    def _install_environment(
        prefix: Prefix,
        version: str,
        additional_dependencies: Sequence[str],
    ) -> None:
        import logging  # noqa: PLC0415

        from pre_commit.lang_base import environment_dir, setup_cmd  # noqa: PLC0415
        from pre_commit.util import cmd_output_b  # noqa: PLC0415

        logger = logging.getLogger("pre_commit")
        logger.info("Using pre-commit with uv %s via pre-commit-uv %s", uv_version(), self_version())
        uv = _uv()
        venv_cmd = [uv, "venv", environment_dir(prefix, python.ENVIRONMENT_DIR, version)]
        py = python.norm_version(version)
        if py is not None:
            venv_cmd.extend(("-p", py))
        env = os.environ.copy()
        env["UV_INTERNAL__PARENT_INTERPRETER"] = sys.executable
        cmd_output_b(*venv_cmd, cwd="/", env=env)

        with python.in_env(prefix, version):
            setup_cmd(prefix, (uv, "pip", "install", ".", *additional_dependencies))

    @cache
    def _uv() -> str:
        from uv import find_uv_bin  # noqa: PLC0415

        return find_uv_bin()

    @cache
    def self_version() -> str:
        from importlib.metadata import version as _metadata_version  # noqa: PLC0415

        return _metadata_version("pre-commit-uv")

    @cache
    def uv_version() -> str:
        from importlib.metadata import version as _metadata_version  # noqa: PLC0415

        return _metadata_version("uv")

    @cache
    def _version_info(exe: str) -> str:
        from pre_commit.util import CalledProcessError, cmd_output  # noqa: PLC0415

        prog = 'import sys;print(".".join(str(p) for p in sys.version_info[0:3]))'
        try:
            return cast(str, cmd_output(exe, "-S", "-c", prog)[1].strip())
        except CalledProcessError:
            return f"<<error retrieving version from {exe}>>"

    python.install_environment = _install_environment
    python._version_info = _version_info  # noqa: SLF001
    assert _original_main is not None  # noqa: S101
    return cast(int, _original_main(argv))
