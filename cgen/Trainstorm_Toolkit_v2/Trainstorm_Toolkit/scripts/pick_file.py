"""
pick_file.py
Minimal tkinter file browser. Prints the selected file path to stdout.

Usage:
  python pick_file.py "Title of dialog" "docx"     <- one or more extensions
  python pick_file.py "Pick a workbook" "xlsx" "xls"

Prints CANCELLED and exits 1 if the user closes the dialog.
"""
import sys
import tkinter as tk
from tkinter import filedialog

title = sys.argv[1] if len(sys.argv) > 1 else "Select a file"
exts = [e.lstrip(".").lower() for e in sys.argv[2:]] or ["*"]

filetypes = [(f".{e} files", f"*.{e}") for e in exts]
filetypes.append(("All files", "*.*"))

root = tk.Tk()
root.withdraw()
root.lift()
root.attributes("-topmost", True)

path = filedialog.askopenfilename(title=title, filetypes=filetypes)

if path:
    print(path.replace("/", "\\"))
    sys.exit(0)
else:
    print("CANCELLED")
    sys.exit(1)
