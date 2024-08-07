"""For editable installs the pth file is not applied, so we have to manually add it."""  # noqa: INP001

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
shutil.copy2(ROOT / "src" / "pre_commit_uv_patch.pth", sys.argv[1])
