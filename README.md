<div align="center">
  <img src="logo.png" alt="MKQ Github Automator Logo" width="120" />
  <h1>MKQ - GitHub Automation Tool</h1>
  <p><strong>A sleek, high-performance desktop application for automating GitHub repository management.</strong></p>
  
  [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()
  [![Python](https://img.shields.io/badge/Python-3.x-blue.svg)]()
</div>

<hr />

## 📖 Overview

The **MKQ GitHub Automation Tool** is a professional desktop utility built to streamline and accelerate how developers interact with GitHub repositories. Engineered with a beautiful, dark-themed Cyberpunk UI, it provides a centralized interface for downloading, cloning, categorizing, and extracting raw code from both public and private repositories.

## ✨ Key Features

- **Intelligent Auto-Organizer**  
  Automatically analyzes the contents of downloaded or cloned repositories, detects the primary programming environment (e.g., Python, C#, Web Technologies), and organizes them into neatly categorized directories.

- **Seamless Repository Cloning & Downloading**  
  Supports direct Git cloning or standard ZIP extraction. Simply paste a repository URL, and the tool handles the entire fetching and extraction pipeline in the background.

- **Secure Private Repository Access**  
  Securely integrate your GitHub Personal Access Token (PAT) to seamlessly clone and extract raw files from your private repositories without repetitive authentication prompts.

- **Instant Code Extractor**  
  Bypass the browser entirely. Paste a standard GitHub file URL or raw content link, and the tool will instantly fetch the raw source code and inject it directly into your system's clipboard.

- **Persistent Configuration Management**  
  Features a dedicated settings modal to configure default download directories and securely store access tokens across sessions.

## 🚀 Installation & Setup

### Option 1: Standalone Executable (Windows)
For the quickest setup on Windows environments, download the pre-compiled executable directly.
1. Download `MKQ - Github Automation Tool - Public.exe` from this repository.
2. Run the application (No installation required).

### Option 2: Running from Source
To run the application via Python:

1. Clone the repository:
   ```bash
   git clone https://github.com/mkjq/MKQ-Github-Automator.git
   cd MKQ-Github-Automator
   ```
2. Install the required dependencies:
   ```bash
   pip install customtkinter Pillow requests
   ```
3. Execute the core script:
   ```bash
   python main.py
   ```

### 🛠 Compiling from Source
To compile your own standalone Windows executable:
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --clean --name="MKQ - Github Automation Tool" --icon="icon.ico" --add-data "icon.ico;." --add-data "logo.png;." --collect-all customtkinter main.py
```

## ⚖️ License & Copyright

This project is open-source and released under the **MIT License**. 

**Proprietary Branding Exception:**
Please note that while the source code is MIT Licensed, the name **"MKQ"** and the associated project logos (`icon.ico`, `logo.png`) are the exclusive intellectual property of **Mohammad Khaled Qatanany**. These branding assets are strictly excluded from the open-source license and may not be used, distributed, or modified in any derivative works or forks without explicit written authorization.

<hr />

<div align="center">
  <p>Developed and maintained by <strong><a href="https://github.com/mkjq">Mohammad Khaled Qatanany</a></strong></p>
</div>
