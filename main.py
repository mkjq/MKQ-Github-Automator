import os
import sys
import shutil
import threading
import subprocess
import zipfile
import urllib.request
import urllib.error
import time
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / "Documents" / "MKQ_Automator"
        self.config_file = self.config_dir / "config.json"
        
        # Default configuration
        self.config = {
            "download_path": str(Path.home() / "Downloads" / "Github_Projects"),
            "github_pat": "",
            "save_pat": False
        }
        self.load()
        
    def load(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.config.update(saved)
        except Exception:
            pass
            
    def save(self):
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

class GitHubAutomatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MKQ - Github Automation Tool")
        self.geometry("850x700")
        
        self.config_mgr = ConfigManager()
        
        # Load custom window icon (handles PyInstaller temp directory)
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
            
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        
        # Visual Theme & Color Palette (GitHub Copilot / Cyberpunk Style)
        self.bg_color = "#0d0e15"               # Deep Background
        self.primary_accent = "#8a2be2"         # Cyber Purple
        self.primary_hover = "#9b51e0"          # Cyber Purple Lighter
        self.secondary_accent = "#00f0ff"       # Neon Electric Blue/Cyan
        self.text_header = "#ffffff"            # Crisp White
        self.text_label = "#a9b2c3"             # Soft Silver/Gray
        self.frame_bg = "#161824"               # Lighter than bg
        self.entry_bg = "#1a1c29"               # Entry background
        
        # Configure the main window appearance
        self.configure(fg_color=self.bg_color)
        ctk.set_appearance_mode("dark")
        
        # Context Menu Helper
        def _add_context_menu(entry_widget):
            menu = tk.Menu(self, tearoff=0, bg=self.entry_bg, fg=self.text_header, activebackground=self.primary_accent, activeforeground=self.text_header)
            menu.add_command(label="Paste", command=lambda: entry_widget.event_generate("<<Paste>>"))
            menu.add_command(label="Copy", command=lambda: entry_widget.event_generate("<<Copy>>"))
            menu.add_command(label="Select All", command=lambda: entry_widget.select_range(0, 'end'))
            
            def show_menu(event):
                menu.tk_popup(event.x_root, event.y_root)
                
            def force_paste(event):
                try:
                    entry_widget.insert("insert", self.clipboard_get())
                    return "break"
                except:
                    pass
                    
            entry_widget.bind("<Button-3>", show_menu)
            entry_widget.bind("<Control-v>", force_paste)
            
        self._add_context_menu = _add_context_menu
        
        # Initialize UI Components
        self.setup_ui()

    def setup_ui(self):
        """Builds the Cyberpunk-styled UI layout."""
        # Main Container
        self.main_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Settings Button (Top Right)
        self.settings_btn = ctk.CTkButton(
            self.main_frame, 
            text="⚙️ Settings", 
            width=100, 
            font=("Inter", 12, "bold"),
            fg_color="transparent", 
            hover_color=self.frame_bg,
            border_width=1,
            border_color=self.secondary_accent,
            text_color=self.text_label,
            command=self.open_settings
        )
        self.settings_btn.place(relx=0.98, rely=0.01, anchor="ne")
        
        # Logo Image
        def resource_path(relative_path):
            try: return os.path.join(sys._MEIPASS, relative_path)
            except Exception: return os.path.join(os.path.abspath("."), relative_path)
            
        try:
            logo_path = resource_path("logo.png")
            self.logo_img = ctk.CTkImage(light_image=Image.open(logo_path),
                                         dark_image=Image.open(logo_path),
                                         size=(64, 64))
            self.logo_label = ctk.CTkLabel(self.main_frame, image=self.logo_img, text="")
            self.logo_label.pack(pady=(10, 5))
        except Exception:
            pass
            
        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="MKQ - GITHUB AUTOMATION TOOL", 
            font=("Inter", 28, "bold"), 
            text_color=self.text_header
        )
        self.header_label.pack(pady=(0, 20))

        # ---------------------------------------------------------
        # MODULE 1: SMART DOWNLOADER & AUTO-ORGANIZER
        # ---------------------------------------------------------
        self.downloader_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=self.frame_bg,
            border_color=self.secondary_accent,
            border_width=1,
            corner_radius=10
        )
        self.downloader_frame.pack(fill="x", padx=10, pady=10)
        
        self.dl_title = ctk.CTkLabel(
            self.downloader_frame, 
            text="Smart Downloader & Auto-Organizer", 
            font=("Inter", 18, "bold"), 
            text_color=self.text_header
        )
        self.dl_title.pack(pady=(15, 10), padx=20, anchor="w")

        self.dl_input_frame = ctk.CTkFrame(self.downloader_frame, fg_color="transparent")
        self.dl_input_frame.pack(fill="x", padx=20, pady=5)

        self.repo_url_entry = ctk.CTkEntry(
            self.dl_input_frame, 
            placeholder_text="Enter GitHub Repository URL or ZIP link...",
            placeholder_text_color=self.text_label,
            fg_color=self.entry_bg,
            border_color=self.secondary_accent,
            text_color=self.text_header,
            font=("Inter", 14),
            height=40,
            corner_radius=6
        )
        self.repo_url_entry.pack(fill="x", pady=5)
        self._add_context_menu(self.repo_url_entry)

        self.download_btn = ctk.CTkButton(
            self.downloader_frame, 
            text="Download / Clone", 
            command=self.start_download,
            fg_color=self.primary_accent,
            hover_color=self.primary_hover,
            text_color=self.text_header,
            font=("Inter", 14, "bold"),
            height=40,
            corner_radius=6
        )
        self.download_btn.pack(pady=10, padx=20, anchor="e")

        self.progress_bar = ctk.CTkProgressBar(
            self.downloader_frame, 
            progress_color=self.secondary_accent,
            fg_color=self.bg_color,
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(5, 0))
        self.progress_bar.set(0)

        self.dl_status_label = ctk.CTkLabel(
            self.downloader_frame, 
            text="Status: Waiting for input...", 
            font=("Inter", 12), 
            text_color=self.text_label
        )
        self.dl_status_label.pack(pady=(5, 15), padx=20, anchor="w")

        # ---------------------------------------------------------
        # MODULE 2: CODE EXTRACTOR
        # ---------------------------------------------------------
        self.extractor_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=self.frame_bg,
            border_color=self.secondary_accent,
            border_width=1,
            corner_radius=10
        )
        self.extractor_frame.pack(fill="x", padx=10, pady=20)
        
        self.ex_title = ctk.CTkLabel(
            self.extractor_frame, 
            text="Code Extractor", 
            font=("Inter", 18, "bold"), 
            text_color=self.text_header
        )
        self.ex_title.pack(pady=(15, 10), padx=20, anchor="w")

        self.code_url_entry = ctk.CTkEntry(
            self.extractor_frame, 
            placeholder_text="Enter raw code file URL or standard GitHub file view URL...",
            placeholder_text_color=self.text_label,
            fg_color=self.entry_bg,
            border_color=self.secondary_accent,
            text_color=self.text_header,
            font=("Inter", 14),
            height=40,
            corner_radius=6
        )
        self.code_url_entry.pack(fill="x", padx=20, pady=5)
        self._add_context_menu(self.code_url_entry)

        self.extract_btn = ctk.CTkButton(
            self.extractor_frame, 
            text="Fetch & Copy to Clipboard", 
            command=self.start_extraction,
            fg_color=self.primary_accent,
            hover_color=self.primary_hover,
            text_color=self.text_header,
            font=("Inter", 14, "bold"),
            height=40,
            corner_radius=6
        )
        self.extract_btn.pack(pady=10, padx=20, anchor="e")

        self.ex_toast_label = ctk.CTkLabel(
            self.extractor_frame, 
            text="", 
            font=("Inter", 14, "bold"), 
            text_color=self.secondary_accent
        )
        self.ex_toast_label.pack(pady=(0, 15), padx=20, anchor="w")
        
        # ---------------------------------------------------------
        # FOOTER (Open Source Identity)
        # ---------------------------------------------------------
        self.footer_label = ctk.CTkLabel(
            self.main_frame,
            text="© 2026 MKQ | Open Source GitHub Automation Tool",
            font=("Inter", 10),
            text_color=self.text_label
        )
        self.footer_label.pack(side="bottom", pady=5)

    # ==========================================
    # SETTINGS MODAL
    # ==========================================
    def open_settings(self):
        settings_win = ctk.CTkToplevel(self)
        settings_win.title("Settings")
        settings_win.geometry("500x440")
        settings_win.configure(fg_color=self.bg_color)
        settings_win.transient(self) # Keep on top of main
        settings_win.grab_set() # Make modal
        
        if hasattr(self, 'logo_img'):
            logo_label = ctk.CTkLabel(settings_win, image=self.logo_img, text="")
            logo_label.pack(pady=(15, 0))
        
        title = ctk.CTkLabel(settings_win, text="Application Settings", font=("Inter", 18, "bold"), text_color=self.text_header)
        title.pack(pady=10)
        
        # Path Config
        path_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(path_frame, text="Download Directory:", text_color=self.text_label).pack(anchor="w")
        
        path_inner = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_inner.pack(fill="x")
        
        path_entry = ctk.CTkEntry(path_inner, fg_color=self.entry_bg, border_color=self.secondary_accent, text_color=self.text_header)
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        path_entry.insert(0, self.config_mgr.config.get("download_path", ""))
        self._add_context_menu(path_entry)
        
        def browse_path():
            selected = filedialog.askdirectory(initialdir=path_entry.get())
            if selected:
                path_entry.delete(0, "end")
                path_entry.insert(0, selected)
                
        ctk.CTkButton(path_inner, text="Browse", width=80, fg_color=self.frame_bg, hover_color=self.primary_accent, command=browse_path).pack(side="right")
        
        # Token Config
        token_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        token_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(token_frame, text="GitHub Personal Access Token (Optional):", text_color=self.text_label).pack(anchor="w")
        token_entry = ctk.CTkEntry(token_frame, show="*", fg_color=self.entry_bg, border_color=self.secondary_accent, text_color=self.text_header)
        token_entry.pack(fill="x")
        
        if self.config_mgr.config.get("save_pat"):
            token_entry.insert(0, self.config_mgr.config.get("github_pat", ""))
            
        self._add_context_menu(token_entry)
        
        # Save PAT Checkbox
        save_pat_var = ctk.BooleanVar(value=self.config_mgr.config.get("save_pat", False))
        ctk.CTkCheckBox(
            token_frame, 
            text="Save Token securely", 
            variable=save_pat_var, 
            text_color=self.text_label,
            fg_color=self.primary_accent,
            hover_color=self.primary_hover
        ).pack(anchor="w", pady=10)
        
        def save_and_close():
            self.config_mgr.config["download_path"] = path_entry.get().strip()
            self.config_mgr.config["save_pat"] = save_pat_var.get()
            if save_pat_var.get():
                self.config_mgr.config["github_pat"] = token_entry.get().strip()
            else:
                self.config_mgr.config["github_pat"] = ""
            self.config_mgr.save()
            settings_win.destroy()
            
        ctk.CTkButton(
            settings_win, 
            text="Save Settings", 
            fg_color=self.primary_accent, 
            hover_color=self.primary_hover,
            font=("Inter", 14, "bold"),
            command=save_and_close
        ).pack(pady=20)

    # ==========================================
    # LOGIC: SMART DOWNLOADER & AUTO-ORGANIZER
    # ==========================================
    def get_pat(self):
        return self.config_mgr.config.get("github_pat", "") if self.config_mgr.config.get("save_pat", False) else ""

    def start_download(self):
        url = self.repo_url_entry.get().strip()
        pat = self.get_pat()
        
        if not url:
            self.dl_status_label.configure(text="Status: Error - Please enter a Repository URL.", text_color="red")
            return
            
        self.dl_status_label.configure(text="Status: Initializing...", text_color=self.secondary_accent)
        self.download_btn.configure(state="disabled")
        self.progress_bar.set(0.1)
        
        threading.Thread(target=self._download_thread, args=(url, pat), daemon=True).start()
        
    def _download_thread(self, url, pat):
        try:
            self._update_progress(0.2, "Status: Resolving URL...")
            
            # Use dynamic root path from settings
            root_path = Path(self.config_mgr.config.get("download_path", str(Path.home() / "Downloads" / "Github_Projects")))
            root_path.mkdir(parents=True, exist_ok=True)
            
            is_zip = False
            if url.endswith(".zip"):
                is_zip = True
                parts = url.split("/")
                project_name = parts[-3] if "archive" in parts else parts[-1].replace(".zip", "")
            else:
                parts = [p for p in url.split("/") if p]
                project_name = parts[-1]
                if project_name.endswith(".git"): project_name = project_name[:-4]
            
            target_dir = root_path / project_name
            if target_dir.exists():
                target_dir = root_path / f"{project_name}_{int(time.time())}"
            
            if is_zip:
                self._update_progress(0.4, "Status: Downloading and Extracting ZIP...")
                import tempfile
                
                req = urllib.request.Request(url)
                if pat:
                    req.add_header("Authorization", f"token {pat}")
                req.add_header("User-Agent", "Mozilla/5.0")
                
                with urllib.request.urlopen(req) as response:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                        shutil.copyfileobj(response, tmp)
                        tmp_path = tmp.name
                
                with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                    zip_ref.extractall(root_path)
                    extracted_names = zip_ref.namelist()
                    if extracted_names:
                        root_folder = extracted_names[0].split('/')[0]
                        target_dir = root_path / root_folder
                os.remove(tmp_path)
            else:
                self._update_progress(0.4, "Status: Cloning Git Repository...")
                clone_url = url
                if pat and "github.com" in clone_url and not "@" in clone_url:
                    clone_url = clone_url.replace("https://github.com/", f"https://{pat}@github.com/")
                
                cmd = ["git", "clone", clone_url, str(target_dir)]
                try:
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                except FileNotFoundError:
                    self._update_progress(0.4, "Status: Git not installed. Falling back to ZIP...")
                    import tempfile
                    parts = [p for p in url.split("/") if p]
                    if len(parts) >= 4 and parts[1] == "github.com":
                        repo_name = parts[3].replace(".git", "")
                        api_url = f"https://api.github.com/repos/{parts[2]}/{repo_name}/zipball"
                        req = urllib.request.Request(api_url)
                        if pat:
                            req.add_header("Authorization", f"token {pat}")
                        req.add_header("User-Agent", "Mozilla/5.0")
                        with urllib.request.urlopen(req) as response:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                                shutil.copyfileobj(response, tmp)
                                tmp_path = tmp.name
                        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                            zip_ref.extractall(root_path)
                            extracted_names = zip_ref.namelist()
                            if extracted_names:
                                root_folder = extracted_names[0].split('/')[0]
                                target_dir = root_path / root_folder
                        os.remove(tmp_path)
                    else:
                        raise Exception("Git not installed and URL is not a standard GitHub repository.")
                
            self._update_progress(0.8, "Status: Organizing Files...")
            
            category = self.get_category(target_dir)
            final_dest_dir = root_path / category
            final_dest_dir.mkdir(parents=True, exist_ok=True)
            
            final_path = final_dest_dir / target_dir.name
            if final_path.exists():
                final_path = final_dest_dir / f"{target_dir.name}_{int(time.time())}"
                
            shutil.move(str(target_dir), str(final_path))
            
            self._update_progress(1.0, f"Status: Done! Project saved into {category}")
            
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() if e.stderr else "Git clone failed."
            self._update_progress(0.0, f"Status: Error - {err_msg[:60]}...")
        except Exception as e:
            self._update_progress(0.0, f"Status: Error - {str(e)[:60]}")
        finally:
            self.after(0, lambda: self.download_btn.configure(state="normal"))
            
    def _update_progress(self, val, text):
        self.after(0, lambda: self.progress_bar.set(val))
        self.after(0, lambda: self.dl_status_label.configure(text=text, text_color=self.secondary_accent if "Error" not in text else "red"))

    def get_category(self, folder_path):
        folder = Path(folder_path)
        files_to_check = []
        try:
            for item in folder.iterdir():
                if item.is_file():
                    files_to_check.append(item)
                elif item.is_dir() and not item.name.startswith('.'):
                    for sub_item in item.iterdir():
                        if sub_item.is_file():
                            files_to_check.append(sub_item)
        except Exception:
            return "General"
            
        extensions = {f.suffix.lower() for f in files_to_check}
        names = {f.name.lower() for f in files_to_check}
        
        if ".gml" in extensions or "project.yyp" in names: return "GameMaker"
        if ".sln" in extensions or ".csproj" in extensions or ".cs" in extensions: return "CSharp"
            
        web_indicators = {"package.json", "index.html", "webpack.config.js", "vite.config.js"}
        web_exts = {".html", ".css", ".js", ".ts", ".jsx", ".tsx"}
        if names.intersection(web_indicators) or extensions.intersection(web_exts): return "Web"
            
        if ".py" in extensions: return "Python"
        return "General"

    # ==========================================
    # LOGIC: CODE EXTRACTOR
    # ==========================================
    def start_extraction(self):
        url = self.code_url_entry.get().strip()
        if not url: return
            
        if "github.com" in url and "/blob/" in url:
            url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            
        self.extract_btn.configure(state="disabled")
        self.ex_toast_label.configure(text="Fetching...", text_color=self.text_label)
        
        pat = self.get_pat()
        threading.Thread(target=self._extract_thread, args=(url, pat), daemon=True).start()
        
    def _extract_thread(self, url, pat):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0")
            
            if pat and "raw.githubusercontent.com" in url:
                req.add_header("Authorization", f"token {pat}")

            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
            self.after(0, lambda: self._copy_to_clipboard(content))
        except urllib.error.HTTPError as e:
            self.after(0, lambda: self._show_extractor_toast(f"HTTP Error: {e.code}", "red"))
        except Exception as e:
            self.after(0, lambda: self._show_extractor_toast(f"Error: {str(e)[:40]}", "red"))
        finally:
            self.after(0, lambda: self.extract_btn.configure(state="normal"))

    def _copy_to_clipboard(self, content):
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update() 
        self._show_extractor_toast("Code copied to clipboard!", self.secondary_accent)
        
    def _show_extractor_toast(self, msg, color):
        self.ex_toast_label.configure(text=msg, text_color=color)
        self.after(3000, lambda: self.ex_toast_label.configure(text=""))

if __name__ == "__main__":
    app = GitHubAutomatorApp()
    app.mainloop()
