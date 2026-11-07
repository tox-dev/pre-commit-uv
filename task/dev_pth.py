"""For editable installs the pth file is not applied, so we have to manually add it."""  # ruff:ignore[implicit-namespace-package]

from __future__ import annotations

import shutil
import sys
from pathlib import Path

_ROOT = Path(__file__).parents[1]
shutil.copy2(_ROOT / "src" / "pre_commit_uv_patch.pth", sys.argv[1])
