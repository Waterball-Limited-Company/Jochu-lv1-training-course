# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import runpy
from pathlib import Path


TARGET = (
    Path(__file__).resolve().parents[2]
    / "analyze"
    / "scripts"
    / "validate_api_contract_references.py"
)


if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
