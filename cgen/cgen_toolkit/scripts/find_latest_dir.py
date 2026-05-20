"""
find_latest_dir.py
Finds the most recently modified subdirectory of a given path.
Prints the full path, or NOT_FOUND if none exist.
Called by cgen_build.bat to locate the timestamped output folder
from file_to_structured_all_md.py without using PowerShell.
"""
import os
import sys

if len(sys.argv) < 2:
    print("NOT_FOUND")
    sys.exit(1)

parent = sys.argv[1]

if not os.path.isdir(parent):
    print("NOT_FOUND")
    sys.exit(1)

subdirs = [
    os.path.join(parent, d)
    for d in os.listdir(parent)
    if os.path.isdir(os.path.join(parent, d))
]

if not subdirs:
    print("NOT_FOUND")
    sys.exit(1)

latest = max(subdirs, key=os.path.getmtime)
print(latest)
sys.exit(0)
