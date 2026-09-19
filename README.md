# SQLDiff UI

A lightweight, user-friendly graphical interface (GUI) built with Python and [Tkinter](https://docs.python.org/3/library/tkinter.html) to compare [SQLite](https://www.sqlite.org) databases. This tool wraps around the official SQLite [`sqldiff`](https://www.sqlite.org/sqldiff.html) utility, eliminating the need to use the command line for database diffing.

![](docs/img/ui.png)

## Features

- **Graphical File Selection:** Easily browse and select your SQLite database files and the `sqldiff` executable.
- **Configurable Diff Flags:** Toggle official `sqldiff` options directly from the UI:
  - `--primarykey`: Use the primary key instead of rowid (enabled by default).
  - `--schema`: Compare database schemas only.
  - `--summary`: Show a summary of differences.
  - `--transaction`: Wrap the output script in a transaction.

## Configuration

To use this tool, you must download the **sqlite-tools** bundle from the [official SQLite downloads page](https://www.sqlite.org/download.html). For the application to detect it automatically, the `sqldiff` executable needs to be available in your system's `PATH`.

Follow the instructions below according to your operating system:

### Windows

1. **Download and Extract:**
   - Download the ZIP file named `sqlite-tools-win-*.zip`.
   - Extract its contents to a permanent folder on your computer (e.g., `C:\sqlite-tools\`).

2. **Add to PATH:**
   - Open the **Start Menu**, search for `"env"`, and select **Edit the system environment variables**.
   - In the System Properties window, click the **Environment Variables...** button at the bottom.
   - Under *System variables* (or *User variables*), locate the **Path** variable and click **Edit...**.
   - Click **New** and paste the full path to the folder where you extracted the tools (e.g., `C:\sqlite-tools\`).
   - Click **OK** on all windows to save the changes.
   - Restart your terminal or application for the changes to take effect.

---

### Linux

Most Linux distributions allow you to install the SQLite development tools directly via your package manager, which configures the `PATH` automatically.

#### Option 1: Via Package Manager (Recommended)

Run the appropriate command for your distribution:

- **Ubuntu / Debian / Mint:**
  ```bash
  sudo apt update
  sudo apt install sqlite3
  ```
- **Fedora / RHEL / CentOS:**
  ```bash
  sudo dnf install sqlite
  ```
- **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S sqlite
  ```

#### Option 2: Manual Installation

If you prefer to download the precompiled binary from the website:

1. Download the `sqlite-tools-linux-*.zip` file and extract it.
2. Move the `sqldiff` binary to a directory already included in your system's `PATH` (e.g., `/usr/local/bin/`):
   ```bash
   sudo mv /path/to/extracted/sqldiff /usr/local/bin/
   sudo chmod +x /usr/local/bin/sqldiff
   ```
## Development

### Setting Up the Environment

This project uses [uv](https://docs.astral.sh/uv). To set up your local development environment and install all required dependencies, run:

```bash
uv sync
```

### Local Builds

The project uses [PyInstaller](https://pyinstaller.org) to package the application into a standalone executable. To build the binary locally for your current operating system, execute the following command:

```bash
uv run pyinstaller --onefile --windowed --name="SqlDiffUI" main.py
```

> 💡 **Note:** Once the build process completes, you can find the generated executable inside the `dist/` directory.

### Publishing a New Version

Production releases are automated via GitHub Actions. The CI/CD workflow triggers automatically whenever a new version tag is pushed to the repository.
To publish a new release, follow these steps:

1. **Create a new version tag** (ensure it follows the [semantic versioning format](https://semver.org) and starts with a `v`):

   ```bash
   git tag v1.0.0
   ```

2. **Push the tag to GitHub** to trigger the automated release workflow:

   ```bash
   git push origin v1.0.0
   ```

The GitHub Action will automatically compile the executables for both Windows and Linux, create a new Release on your repository, and attach the binaries as assets.
