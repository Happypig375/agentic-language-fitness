"""Expose the byte-preserved historical C3 generator under the current package."""

import importlib
import sys

sys.modules[__name__] = importlib.import_module("alf.representation")
