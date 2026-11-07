from __future__ import annotations

import sys
from importlib.metadata import version
from subprocess import check_call, check_output
from textwrap import dedent
from typing import TYPE_CHECKING, Final

import pytest
from pre_commit import main

if TYPE_CHECKING:
    from pathlib import Path

_PRECOMMIT_FILE: Final[str] = ".pre-commit-config.yaml"
_UV: Final[str] = version("uv")
_SELF: Final[str] = version("pre-commit-uv")


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
    check_call(["git", "init"])
    return tmp_path


@pytest.fixture
def install_hook(git_repo: Path) -> None:
    check_call(["pre-commit", "install", "--install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])
    check_call(["pre-commit", "clean"])  # ensures that 'install_environment' gets called


@pytest.mark.usefixtures("install_hook")
def test_run_precommit_hook() -> None:
    hook_result = check_output([".git/hooks/pre-commit"], encoding="utf-8")
    assert f"[INFO] Using pre-commit with uv {_UV} via pre-commit-uv {_SELF}" in hook_result.splitlines()


@pytest.mark.usefixtures("install_hook")
def test_call_as_module() -> None:
    run_result = check_output([sys.executable, "-m", "pre_commit", "run", "-a", "--color", "never"], encoding="utf-8")
    assert f"[INFO] Using pre-commit with uv {_UV} via pre-commit-uv {_SELF}" in run_result.splitlines()


def test_install(git_repo: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    from pre_commit_uv._pre_commit_patch import _patch  # ruff:ignore[import-outside-top-level]

    _patch()
    main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])

    assert caplog.messages == [
        "Initializing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Installing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Once installed this environment will be reused.",
        "This may take a few minutes...",
        f"Using pre-commit with uv {_UV} via pre-commit-uv {_SELF}",
    ]


def test_install_seeds_pip(git_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    from pre_commit_uv._pre_commit_patch import _patch  # ruff:ignore[import-outside-top-level]

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

    from pre_commit_uv._pre_commit_patch import _patch  # ruff:ignore[import-outside-top-level]

    _patch()
    main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])

    assert caplog.messages == [
        "Initializing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Installing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Once installed this environment will be reused.",
        "This may take a few minutes...",
        f"Using pre-commit with uv {_UV} via pre-commit-uv {_SELF}",
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

    from pre_commit_uv._pre_commit_patch import _patch  # ruff:ignore[import-outside-top-level]

    _patch()

    # would raise SystemExit due to bad config
    with pytest.raises(SystemExit):
        main.main(["install-hooks", "-c", str(git_repo / _PRECOMMIT_FILE)])
