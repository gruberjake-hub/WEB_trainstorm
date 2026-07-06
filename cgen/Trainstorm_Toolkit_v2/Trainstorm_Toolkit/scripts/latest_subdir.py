"""
latest_subdir.py
Prints the most recently modified subdirectory of the directory passed
as the first argument. Prints nothing if there are no subdirectories.

Used by cgen_build.bat to find the timestamped output folder created
by Step 1, without relying on fragile inline python -c commands.
"""
import os
import sys

base = sys.argv[1] if len(sys.argv) > 1 else "."

if not os.path.isdir(base):
    sys.exit(0)

dirs = [
    os.path.join(base, d)
    for d in os.listdir(base)
    if os.path.isdir(os.path.join(base, d))
]

if dirs:
    print(max(dirs, key=os.path.getmtime))
