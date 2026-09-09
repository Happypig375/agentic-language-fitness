"""Run the deterministic, model-free H1/H2 construction audit."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from alf.h_check import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
