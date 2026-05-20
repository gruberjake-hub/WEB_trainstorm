"""
pick_folder.py
Minimal tkinter folder browser. Prints the selected path to stdout.
Called by cgen_build.bat to avoid PowerShell dependency on managed machines.
"""
import sys
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.lift()
root.attributes("-topmost", True)

path = filedialog.askdirectory(
    title="Select the project folder to process",
    mustexist=True,
)

if path:
    # Convert forward slashes (tkinter) to backslashes (Windows)
    print(path.replace("/", "\\"))
    sys.exit(0)
else:
    print("CANCELLED")
    sys.exit(1)
