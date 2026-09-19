# SQLDiff UI

A lightweight, user-friendly graphical interface (GUI) built with Python and Tkinter to compare SQLite databases. This tool wraps around the official SQLite `sqldiff` utility, eliminating the need to use the command line for database diffing.

## Features

- **Graphical File Selection:** Easily browse and select your SQLite database files and the `sqldiff` executable.
- **Configurable Diff Flags:** Toggle official `sqldiff` options directly from the UI:
  - `--primarykey`: Use the primary key instead of rowid (enabled by default).
  - `--schema`: Compare database schemas only.
  - `--summary`: Show a summary of differences.
  - `--transaction`: Wrap the output script in a transaction.
