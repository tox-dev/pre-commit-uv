"""Package root."""

from __future__ import annotations

# only import built-ins at top level to avoid interpreter startup overhead
import os
import pathlib
import sys
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Protocol

    from pre_commit.prefix import Prefix

    class _PatchablePython(Protocol):
        install_environment: Callable[[Prefix, str, Sequence[str]], None]
        health_check: Callable[[Prefix, str], str | None]


_original_main = None


def _is_calling_pre_commit() -> bool:
    if "FORCE_PRE_COMMIT_UV_PATCH" in os.environ:
        return True
    if not sys.argv or not sys.argv[0]:
        return False
    # case when pre-commit is called via python -m pre_commit
    if sys.argv[0] == "-m" and "-m" in sys.orig_argv and "pre_commit" in sys.orig_argv:
        return True
    calling = sys.argv[1] if sys.argv[0] == sys.executable and len(sys.argv) >= 1 else sys.argv[0]
    # case when pre-commit is called directly
    if os.path.split(calling)[1] == f"pre-commit{'.exe' if sys.platform == 'win32' else ''}":
        return True
    # case when pre-commit is called due to a git commit
    return "-m" in sys.argv and "hook-impl" in sys.argv


def _patch() -> None:
    global _original_main
    if _original_main is not None:  # already patched, nothing more to do
        return

    if _is_calling_pre_commit() and os.environ.get("DISABLE_PRE_COMMIT_UV_PATCH") is None:
        from pre_commit import main  # noqa: PLC0415

        _original_main, main.main = main.main, _new_main  # ty: ignore[invalid-assignment]
        if "--version" in sys.argv:
            from importlib.metadata import version as _metadata_version  # noqa: PLC0415

            from pre_commit import constants  # noqa: PLC0415

            constants.VERSION = (
                f"{constants.VERSION} ("
                f"pre-commit-uv={_metadata_version('pre-commit-uv')}, "
                f"uv={_metadata_version('uv')}"
                f")"
            )


def _new_main(argv: Sequence[str] | None = None) -> int:
    # imports applied locally to avoid patching import overhead cost
    from functools import cache  # noqa: PLC0415

    from pre_commit.languages import python  # noqa: PLC0415

    def _install_environment(
        prefix: Prefix,
        version: str,
        additional_dependencies: Sequence[str],
    ) -> None:
        import logging  # noqa: PLC0415

        from pre_commit.git import get_root  # noqa: PLC0415
        from pre_commit.lang_base import environment_dir, setup_cmd  # noqa: PLC0415
        from pre_commit.util import cmd_output_b  # noqa: PLC0415

        project_root_dir = get_root()

        logger = logging.getLogger("pre_commit")
        logger.info("Using pre-commit with uv %s via pre-commit-uv %s", uv_version(), self_version())
        uv = _uv()
        py = python.norm_version(version) or os.environ.get("UV_PYTHON", sys.executable)
        venv_cmd = [
            uv,
            "--project",
            project_root_dir,
            "venv",
            "--seed",
            environment_dir(prefix, python.ENVIRONMENT_DIR, version),
            "-p",
            py,
        ]
        cmd_output_b(*venv_cmd, cwd="/")

        with python.in_env(prefix, version):
            setup_cmd(
                prefix,
                (
                    uv,
                    "--project",
                    project_root_dir,
                    "pip",
                    "install",
                    ".",
                    *additional_dependencies,
                ),
            )

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

    patched = cast("_PatchablePython", python)
    patched.install_environment = _install_environment
    patched.health_check = _health_check
    assert _original_main is not None  # noqa: S101
    return _original_main(argv)


def _version_info(exe: str) -> str:
    from pre_commit.util import CalledProcessError, cmd_output  # noqa: PLC0415

    prog = 'import sys;print(".".join(str(p) for p in sys.version_info[0:3]))'
    try:
        return cmd_output(exe, "-S", "-c", prog)[1].strip()
    except CalledProcessError:
        return f"<<error retrieving version from {exe}>>"


def _health_check(prefix: Prefix, version: str) -> str | None:
    # uv may record fewer version components in pyvenv.cfg than pre-commit expects (e.g. "3.14" vs "3.14.6"),
    # so compare only the components uv actually wrote rather than requiring an exact string match
    from pre_commit.lang_base import environment_dir  # noqa: PLC0415
    from pre_commit.languages import python  # noqa: PLC0415
    from pre_commit.util import win_exe  # noqa: PLC0415

    pyvenv_cfg = pathlib.Path(environment_dir(prefix, python.ENVIRONMENT_DIR, version)) / "pyvenv.cfg"
    if not pyvenv_cfg.exists():
        return "pyvenv.cfg does not exist (old virtualenv?)"

    cfg = python._read_pyvenv_cfg(str(pyvenv_cfg))  # noqa: SLF001
    if "version_info" not in cfg:
        return "created virtualenv's pyvenv.cfg is missing `version_info`"
    expected = cfg["version_info"].split(".")

    py_exe = prefix.path(python.bin_dir(str(pyvenv_cfg.parent)), win_exe("python"))
    targets = [("virtualenv python", py_exe)]
    if "base-executable" in cfg:
        targets.append(("base executable", cfg["base-executable"]))
    for label, exe in targets:
        if (actual := _version_info(exe)).split(".")[: len(expected)] != expected:
            return (
                f"{label} version did not match created version:\n"
                f"- actual version: {actual}\n"
                f"- expected version: {cfg['version_info']}\n"
            )
    return None
