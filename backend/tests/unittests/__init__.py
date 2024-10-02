import os
import sys
from pathlib import Path

dirname = os.path.dirname(os.path.realpath(__file__))
while dirname != "/":
    files_and_dirs = os.listdir(dirname)
    if "src" in files_and_dirs:
        sys.path.append(str(Path(dirname) / "src"))
        break
    dirname = str((Path(dirname) / "..").resolve())
else:
    raise RuntimeError("Couldn't find root directory")
