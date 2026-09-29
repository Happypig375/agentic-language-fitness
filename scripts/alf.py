"""Compatibility launcher for recorded ALF commands; use scripts/ise.py now."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ise.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
