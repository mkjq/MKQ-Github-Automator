# MKQ - Github Automation Tool

A beautiful, dark-themed, desktop application written in Python and CustomTkinter. 
This tool simplifies interacting with GitHub repositories by allowing you to easily download, clone, auto-organize, and extract raw code from public or private repositories.

**Developed with ❤️ by [Mohammad Khaled Qatanany (mkjq)](https://github.com/mkjq)**

## Features
- **Smart Downloader & Auto-Organizer:** Automatically detects the programming language of a repository and organizes it into neat folders (e.g., Python, CSharp, Web).
- **Code Extractor:** Quickly fetches raw code from a GitHub URL and copies it straight to your clipboard.
- **Private Repository Support:** Authenticate securely using a GitHub Personal Access Token (PAT).
- **Persistent Settings:** Save your token securely and customize your default download directory.
- **Cyberpunk UI:** Built with CustomTkinter for a sleek, modern look.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mkjq/MKQ-Github-Automator.git
   ```
2. Install the required dependencies:
   ```bash
   pip install customtkinter Pillow requests
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Compiling to Executable (Windows)

To build a standalone `.exe` file using PyInstaller:
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --clean --name="MKQ - Github Automation Tool - Public" --icon="icon.ico" --add-data "icon.ico;." --add-data "logo.png;." --collect-all customtkinter main.py
```

## License and Copyright Notices

This project is open-source and available under the **MIT License**, with the following strict exceptions:

> **Proprietary Assets Exception:**
> The name **"MKQ"** and the associated project logos (`icon.ico`, `logo.png`) are the exclusive private property of Mohammad Khaled Qatanany. They are strictly excluded from the MIT License. You may not use, distribute, or modify the name "MKQ" or the logos in any derivative works without explicit written permission.
