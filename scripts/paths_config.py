"""
paths_config.py
Central place to configure local tool install paths.
Edit the values below to match your machine — this is the only file
that should need per-OS/per-machine changes.
"""

import platform

SYSTEM = platform.system()  # "Windows", "Darwin" (Mac), or "Linux"

if SYSTEM == "Windows":
    MGLTOOLS_HOME = r"C:\Program Files (x86)\MGLTools-1.5.7"
    VINA_EXE = r"C:\Users\olami\Documents\vina\vina.exe.exe"
elif SYSTEM == "Darwin":
    MGLTOOLS_HOME = "/Applications/MGLTools-1.5.7"
    VINA_EXE = "/usr/local/bin/vina"
else:  # Linux
    MGLTOOLS_HOME = "/opt/MGLTools-1.5.7"
    VINA_EXE = "/usr/local/bin/vina"

# Derived: MGLTools' bundled Python and the prep scripts, built from MGLTOOLS_HOME above.
# You shouldn't need to edit these directly unless your install layout differs.
MGLTOOLS_PYTHON = f"{MGLTOOLS_HOME}/python.exe" if SYSTEM == "Windows" else f"{MGLTOOLS_HOME}/bin/pythonsh"
UTILITIES_DIR = f"{MGLTOOLS_HOME}/Lib/site-packages/AutoDockTools/Utilities24" if SYSTEM == "Windows" \
    else f"{MGLTOOLS_HOME}/MGLToolsPckgs/AutoDockTools/Utilities24"