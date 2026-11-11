from __future__ import annotations

import sys
from importlib.metadata import version
from shutil import which
from subprocess import check_call, check_output
from textwrap import dedent
from typing import TYPE_CHECKING, Final

import pytest
from pre_commit import main
from pre_commit.languages import python
from pre_commit.prefix import Prefix

from pre_commit_uv._pre_commit_patch import _health_check, _patch

if TYPE_CHECKING:
    from pathlib import Path

_PRECOMMIT_FILE: Final[str] = ".pre-commit-config.yaml"
_UV_VERSION: Final[str] = version("uv")
_PRE_COMMIT_UV_VERSION: Final[str] = version("pre-commit-uv")
_VERSION: Final[str] = "default"
_MAJOR_MINOR: Final[str] = f"{sys.version_info[0]}.{sys.version_info[1]}"
_FULL_VERSION: Final[str] = ".".join(str(p) for p in sys.version_info[0:3])
_WRONG_VERSION: Final[str] = f"{sys.version_info[0]}.{sys.version_info[1] + 1}"


@pytest.fixture
def git_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    conf_file = tmp_path / _PRECOMMIT_FILE
    conf = """
    repos:
      - repo: https://github.com/tox-dev/pyproject-fmt
        rev: "2.2.0"
        hooks:
          - id: pyproject-fmt
    """
    conf_file.write_text(dedent(conf))
    monkeypatch.setenv("PRE_COMMIT_HOME", str(tmp_path / "store"))
    monkeypatch.chdir(tmp_path)
    git = which("git")
    assert git is not None
    check_call([git, "init"])
    return tmp_path


@pytest.fixture
def install_hook(git_repo: Path) -> None:
    pre_commit = which("pre-commit")
    assert pre_commit is not None
    check_call([pre_commit, "install", "--install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])
    check_call([pre_commit, "clean"])  # ensures that 'install_environment' gets called


@pytest.mark.usefixtures("install_hook")
def test_run_precommit_hook(git_repo: Path) -> None:
    hook_result = check_output([str(git_repo / ".git" / "hooks" / "pre-commit")], encoding="utf-8")
    assert (
        f"[INFO] Using pre-commit with uv {_UV_VERSION} via pre-commit-uv {_PRE_COMMIT_UV_VERSION}"
        in hook_result.splitlines()
    )


@pytest.mark.usefixtures("install_hook")
def test_call_as_module() -> None:
    run_result = check_output([sys.executable, "-m", "pre_commit", "run", "-a", "--color", "never"], encoding="utf-8")
    assert (
        f"[INFO] Using pre-commit with uv {_UV_VERSION} via pre-commit-uv {_PRE_COMMIT_UV_VERSION}"
        in run_result.splitlines()
    )


def test_install(git_repo: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    _patch()
    main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])

    assert caplog.messages == [
        "Initializing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Installing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Once installed this environment will be reused.",
        "This may take a few minutes...",
        f"Using pre-commit with uv {_UV_VERSION} via pre-commit-uv {_PRE_COMMIT_UV_VERSION}",
    ]


def test_install_seeds_pip(git_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    _patch()
    main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])

    env_dirs = list((git_repo / "store").rglob("py_env-*"))
    assert env_dirs, "expected at least one hook environment"
    result = check_output([str(next((env_dirs[0] / "bin").glob("python*"))), "-c", "import pip"], encoding="utf-8")
    assert not result


_TEST_INSTALL_WITH_UV_CONFIG_CASES: Final[list[tuple[str, str]]] = [
    (
        "pyproject.toml",
        """
[[tool.uv.index]]
name = "internal"
url = "https://pypi.org/simple/"
default = true
""",
    ),
    (
        "uv.toml",
        """
[[index]]
name = "internal"
url = "https://pypi.org/simple/"
default = true
""",
    ),
]


@pytest.mark.parametrize(
    ("file_name", "content"),
    _TEST_INSTALL_WITH_UV_CONFIG_CASES,
)
def test_install_with_uv_config(
    git_repo: Path,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    file_name: str,
    content: str,
) -> None:
    (git_repo / file_name).write_text(dedent(content))

    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    _patch()
    main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])

    assert caplog.messages == [
        "Initializing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Installing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Once installed this environment will be reused.",
        "This may take a few minutes...",
        f"Using pre-commit with uv {_UV_VERSION} via pre-commit-uv {_PRE_COMMIT_UV_VERSION}",
    ]


_TEST_INSTALL_WITH_UV_CONFIG_RAISES_ERROR_CASES: Final[list[tuple[str, str]]] = [
    (
        "pyproject.toml",
        """
[[tool.uv.index]]
name = "internal"
url = "https://pypi.example/simple/"
default = true
""",
    ),
    (
        "uv.toml",
        """
[[index]]
name = "internal"
url = "https://pypi.example/simple/"
default = true
""",
    ),
]


@pytest.mark.parametrize(("file_name", "content"), _TEST_INSTALL_WITH_UV_CONFIG_RAISES_ERROR_CASES)
def test_install_with_uv_config_raises_error(
    git_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    file_name: str,
    content: str,
) -> None:
    # Test to make sure that uv config is used for non default pypi repos.
    (git_repo / file_name).write_text(dedent(content))

    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    _patch()

    # would raise SystemExit due to bad config
    with pytest.raises(SystemExit):
        main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])


def test_health_check_truncated_version_passes(tmp_path: Path) -> None:
    # uv >=0.11.22 writes only the major.minor into pyvenv.cfg (see issue #152).
    prefix = _make_env(tmp_path, f"version_info = {_MAJOR_MINOR}\nbase-executable = {sys.executable}\n")

    assert _health_check(prefix, _VERSION) is None


def _make_env(tmp_path: Path, pyvenv_cfg: str | None) -> Prefix:
    envdir = tmp_path / f"py_env-{_VERSION}"
    bin_dir = python.bin_dir(str(envdir))
    (tmp_path / bin_dir).mkdir(parents=True)
    (tmp_path / bin_dir / python.win_exe("python")).symlink_to(sys.executable)
    if pyvenv_cfg is not None:
        (envdir / "pyvenv.cfg").write_text(pyvenv_cfg)
    return Prefix(str(tmp_path))


def test_health_check_full_version_passes(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {_FULL_VERSION}\nbase-executable = {sys.executable}\n")

    assert _health_check(prefix, _VERSION) is None


def test_health_check_no_base_executable_passes(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {_MAJOR_MINOR}\n")

    assert _health_check(prefix, _VERSION) is None


def test_health_check_version_mismatch_fails(tmp_path: Path) -> None:
    result = _health_check(_make_env(tmp_path, f"version_info = {_WRONG_VERSION}\n"), _VERSION)

    assert result is not None
    assert "virtualenv python version did not match created version" in result
    assert f"- expected version: {_WRONG_VERSION}" in result


def test_health_check_base_executable_mismatch_fails(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, f"version_info = {_MAJOR_MINOR}\nbase-executable = /does/not/exist/python\n")

    result = _health_check(prefix, _VERSION)

    assert result is not None
    assert "base executable version did not match created version" in result


def test_health_check_missing_pyvenv_cfg(tmp_path: Path) -> None:
    prefix = _make_env(tmp_path, None)

    assert _health_check(prefix, _VERSION) == "pyvenv.cfg does not exist (old virtualenv?)"


@pytest.mark.parametrize(
    "contents",
    [
        pytest.param("# comment\nhome = /usr\n", id="no-version"),
        pytest.param("version_info = 3=15\n", id="extra-equals"),
    ],
)
def test_health_check_missing_version_info(tmp_path: Path, contents: str) -> None:
    prefix = _make_env(tmp_path, contents)

    assert _health_check(prefix, _VERSION) == "created virtualenv's pyvenv.cfg is missing `version_info`"
