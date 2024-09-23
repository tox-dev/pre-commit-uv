from __future__ import annotations

from importlib.metadata import version
from subprocess import check_call, check_output
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest
from pre_commit import main

if TYPE_CHECKING:
    from pathlib import Path

precommit_file = ".pre-commit-config.yaml"
uv = version("uv")
self = version("pre-commit-uv")


@pytest.fixture
def git_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    conf = """
    repos:
      - repo: https://github.com/tox-dev/pyproject-fmt
        rev: "2.2.0"
        hooks:
          - id: pyproject-fmt
    """
    conf_file = tmp_path / precommit_file
    conf_file.write_text(dedent(conf))
    monkeypatch.setenv("PRE_COMMIT_HOME", str(tmp_path / "store"))
    monkeypatch.chdir(tmp_path)
    check_call(["git", "init"])
    return tmp_path


@pytest.fixture
def install_hook(git_repo: Path) -> None:
    check_call(["pre-commit", "install", "--install-hooks", "-c", str(git_repo / precommit_file)])
    check_call(["pre-commit", "clean"])  # ensures that 'install_environment' gets called


@pytest.mark.usefixtures("install_hook")
def test_run_precommit_hook() -> None:
    hook_result = check_output([".git/hooks/pre-commit"], encoding="utf-8")
    assert f"[INFO] Using pre-commit with uv {uv} via pre-commit-uv {self}" in hook_result.splitlines()


@pytest.mark.usefixtures("install_hook")
def test_call_as_module() -> None:
    run_result = check_output(["python3", "-m", "pre_commit", "run", "-a", "--color", "never"], encoding="utf-8")
    assert f"[INFO] Using pre-commit with uv {uv} via pre-commit-uv {self}" not in run_result.splitlines()


def test_install(git_repo: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_PRE_COMMIT_UV_PATCH", "1")

    import pre_commit_uv  # noqa: PLC0415

    pre_commit_uv._patch()  # noqa: SLF001
    main.main(["install-hooks", "-c", str(git_repo / precommit_file)])

    assert caplog.messages == [
        "Initializing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Installing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Once installed this environment will be reused.",
        "This may take a few minutes...",
        f"Using pre-commit with uv {uv} via pre-commit-uv {self}",
    ]
