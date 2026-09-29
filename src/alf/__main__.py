"""Compatibility entry point for historical ``python -m alf`` commands."""

from ise.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
