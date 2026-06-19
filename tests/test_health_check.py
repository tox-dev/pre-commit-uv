from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from pre_commit.languages import python
from pre_commit.prefix import Prefix

from pre_commit_uv import _health_check

if TYPE_CHECKING:
    from pathlib import Path

version = "default"
major_minor = f"{sys.version_info[0]}.{sys.version_info[1]}"
full_version = ".".join(str(p) for p in sys.version_info[0:3])
wrong_version = f"{sys.version_info[0]}.{sys.version_info[1] + 1}"


def _make_env(tmp_path: Path, pyvenv_cfg: str | None) -> Prefix:
    envdir = tmp_path / f"py_env-{version}"
    bin_dir = python.bin_dir(str(envdir))
    (tmp_path / bin_dir).mkdir(parents=True)
    (tmp_path / bin_dir / python.win_exe("python")).symlink_to(sys.executable)
    if pyvenv_cfg is not None:
        (envdir / "pyvenv.cfg").write_text(pyvenv_cfg)
    return Prefix(str(tmp_path))


def test_health_check_truncated_version_passes(tmp_path: Path) -> None:
    """uv >=0.11.22 writes only the major.minor into pyvenv.cfg (see issue #152)."""
    prefix = _make_env(tmp_path, f"version_info = {major_minor}\nbase-executable = {sys.executable}\n")

    assert _health_check(prefix, version) is None


def test_health_check_full_version_passes(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {full_version}\nbase-executable = {sys.executable}\n")

    assert _health_check(prefix, version) is None


def test_health_check_no_base_executable_passes(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {major_minor}\n")

    assert _health_check(prefix, version) is None


def test_health_check_version_mismatch_fails(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {wrong_version}\n")

    result = _health_check(prefix, version)

    assert result is not None
    assert "virtualenv python version did not match created version" in result
    assert f"- expected version: {wrong_version}" in result


def test_health_check_base_executable_mismatch_fails(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {major_minor}\nbase-executable = /does/not/exist/python\n")

    result = _health_check(prefix, version)

    assert result is not None
    assert "base executable version did not match created version" in result


def test_health_check_missing_pyvenv_cfg(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, None)

    assert _health_check(prefix, version) == "pyvenv.cfg does not exist (old virtualenv?)"


def test_health_check_missing_version_info(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, "home = /usr\n")

    assert _health_check(prefix, version) == "created virtualenv's pyvenv.cfg is missing `version_info`"
