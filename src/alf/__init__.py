"""Legacy imports for recorded ALF commands and frozen artifacts.

New code uses :mod:`ise`. The original representation generator remains here
because its source bytes and path are part of the published C3 evidence.
"""

from pathlib import Path

from ise import __version__

__path__.append(str(Path(__file__).resolve().parent.parent / "ise"))
