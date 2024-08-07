from __future__ import annotations

from importlib.metadata import version
from subprocess import check_call
from textwrap import dedent
from typing import TYPE_CHECKING

from pre_commit import main

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_install(tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    conf = """
    repos:
      - repo: https://github.com/tox-dev/pyproject-fmt
        rev: "2.2.0"
        hooks:
          - id: pyproject-fmt
    """
    conf_file = tmp_path / ".pre-commit-config.yaml"
    conf_file.write_text(dedent(conf))
    monkeypatch.setenv("PRE_COMMIT_HOME", str(tmp_path / "store"))
    monkeypatch.chdir(tmp_path)
    check_call(["git", "init"])

    main.main(["install-hooks", "-c", str(conf_file)])

    uv = version("uv")
    self = version("pre-commit-uv")
    assert caplog.messages == [
        "Initializing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Installing environment for https://github.com/tox-dev/pyproject-fmt.",
        "Once installed this environment will be reused.",
        "This may take a few minutes...",
        f"Using pre-commit with uv {uv} via pre-commit-uv {self}",
    ]
