"""
Hunyuan Quickstart Installer - Interactive GUI
Helps users install and configure Tencent Hunyuan AI models
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os
import platform
import json
from pathlib import Path
from typing import Dict, List

class HunyuanInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hunyuan Quickstart Installer")
        self.root.geometry("900x700")
        
        # Configuration
        self.install_dir = Path("D:/Hunyuan") if platform.system() == "Windows" else Path.home() / "Hunyuan"
        self.selected_models = {}
        
        # Model configurations with requirements
        self.models = {
            "HunyuanVideo": {
                "name": "HunyuanVideo (Text-to-Video)",
                "repo": "https://github.com/Tencent-Hunyuan/HunyuanVideo",
                "vram": "60GB",
                "recommended_vram": "80GB"
            },
            "HunyuanVideo-I2V": {
                "name": "HunyuanVideo-I2V (Image-to-Video)",
                "repo": "https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V",
                "vram": "60GB",
                "recommended_vram": "80GB"
            },
            "HunyuanWorld": {
                "name": "HunyuanWorld (3D World Generation)",
                "repo": "https://github.com/Tencent-Hunyuan/HunyuanWorld",
                "vram": "60GB+",
                "recommended_vram": "80GB"
            },
            "Hunyuan3D": {
                "name": "Hunyuan3D (3D Object Generation)",
                "repo": "https://github.com/Tencent-Hunyuan/Hunyuan3D",
                "vram": "20GB",
                "recommended_vram": "40GB"
            },
            "HunyuanDiT": {
                "name": "HunyuanDiT (Image Generation)",
                "repo": "https://github.com/Tencent-Hunyuan/HunyuanDiT",
                "vram": "20GB",
                "recommended_vram": "40GB"
            }
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="🎨 Hunyuan Quickstart Installer",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Select which Hunyuan AI models you want to install",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # Installation Mode
        mode_frame = ttk.LabelFrame(self.root, text="Installation Mode", padding="10")
        mode_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.install_mode = tk.StringVar(value="cloud")
        
        ttk.Radiobutton(
            mode_frame,
            text="🌐 Cloud GPU Setup (RunPod/Vast.ai) - Recommended",
            variable=self.install_mode,
            value="cloud"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            mode_frame,
            text="🖥️ Local Installation (WSL2/Linux)",
            variable=self.install_mode,
            value="local"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            mode_frame,
            text="📦 Dependencies Only (No model weights)",
            variable=self.install_mode,
            value="deps"
        ).pack(anchor=tk.W)
        
        # Model Selection
        model_frame = ttk.LabelFrame(self.root, text="Select Models to Install", padding="10")
        model_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Select All / None
        btn_frame = ttk.Frame(model_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Select None", command=self.select_none).pack(side=tk.LEFT)
        
        # Model checkboxes
        for key, model in self.models.items():
            var = tk.BooleanVar(value=False)
            self.selected_models[key] = var
            
            cb = ttk.Checkbutton(
                model_frame,
                text=f"{model['name']} - Min: {model['vram']}, Rec: {model['recommended_vram']}",
                variable=var
            )
            cb.pack(anchor=tk.W, pady=2)
        
        # Installation Directory
        dir_frame = ttk.Frame(self.root, padding="10")
        dir_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=10)
        
        ttk.Label(dir_frame, text="Installation Directory:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_frame, width=50)
        self.dir_entry.insert(0, str(self.install_dir))
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        
        # Hugging Face Token
        hf_frame = ttk.Frame(self.root, padding="10")
        hf_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=10)
        
        ttk.Label(hf_frame, text="Hugging Face Token (optional):").pack(side=tk.LEFT)
        self.hf_token_entry = ttk.Entry(hf_frame, width=50, show="*")
        self.hf_token_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hf_frame,
            text="Get Token",
            command=self.open_hf_token_page
        ).pack(side=tk.LEFT, padx=5)
        
        # Action Buttons
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        self.install_btn = ttk.Button(
            action_frame,
            text="🚀 Start Installation",
            command=self.start_installation,
            style="Accent.TButton"
        )
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="📖 View Cloud Setup Guide",
            command=self.show_cloud_guide
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="ℹ️ System Info",
            command=self.show_system_info
        ).pack(side=tk.LEFT, padx=5)
        
        # Progress Log
        log_frame = ttk.LabelFrame(self.root, text="Installation Log", padding="10")
        log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.grid(row=7, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(6, weight=2)
        
    def log(self, message: str):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def select_all(self):
        for var in self.selected_models.values():
            var.set(True)
            
    def select_none(self):
        for var in self.selected_models.values():
            var.set(False)
            
    def show_system_info(self):
        """Display system information"""
        info = f"""System Information:
        
OS: {platform.system()} {platform.release()}
Python: {sys.version.split()[0]}
Architecture: {platform.machine()}

GPU Check:
"""
        # Try to detect GPU
        try:
            if platform.system() == "Windows" or self.is_wsl():
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    info += result.stdout
                else:
                    info += "❌ No NVIDIA GPU detected or nvidia-smi not found"
            else:
                info += "Run 'nvidia-smi' to check GPU"
        except Exception as e:
            info += f"❌ Could not check GPU: {e}"
            
        messagebox.showinfo("System Information", info)
        
    def is_wsl(self) -> bool:
        """Check if running in WSL"""
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower()
        except:
            return False
            
    def open_hf_token_page(self):
        """Open Hugging Face token page in browser"""
        import webbrowser
        webbrowser.open("https://huggingface.co/settings/tokens")
            
    def show_cloud_guide(self):
        """Show cloud GPU setup guide"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Cloud GPU Setup Guide")
        guide_window.geometry("700x600")
        
        text = scrolledtext.ScrolledText(guide_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        
        guide_content = """
🌐 CLOUD GPU SETUP GUIDE - RUNPOD

RunPod is the recommended cloud GPU service for Hunyuan models.

STEP 1: Create RunPod Account
1. Go to https://runpod.io/
2. Sign up for a new account
3. Add credits ($10 minimum recommended)

STEP 2: Create GPU Instance
1. Click "Deploy" > "GPU Cloud"
2. Select "A100 80GB" GPU
3. Choose template: "PyTorch 2.0" or "RunPod PyTorch"
4. Set disk space: 200GB+ recommended
5. Click "Deploy On-Demand" or "Deploy Spot" (cheaper)

STEP 3: Connect to Your Instance
1. Wait for pod to start (2-3 minutes)
2. Click "Connect" > "Start Jupyter Lab" or "SSH"
3. Open terminal in Jupyter or SSH

STEP 4: Run This Installer
In the terminal, run:
    git clone https://github.com/YOUR_USERNAME/hunyuan-quickstart
    cd hunyuan-quickstart
    python installer_gui.py

Or use the automated script:
    wget https://raw.githubusercontent.com/YOUR_USERNAME/hunyuan-quickstart/main/cloud_setup/setup_cloud.sh
    chmod +x setup_cloud.sh
    ./setup_cloud.sh

COSTS:
- A100 80GB On-Demand: ~$1.89/hour
- A100 80GB Spot: ~$1.29/hour (can be interrupted)
- Storage: ~$0.10/GB/month

TIPS:
✅ Use Spot instances for experimentation (cheaper)
✅ Stop pod when not in use to save money
✅ Download results before stopping pod
✅ Use persistent volumes for model weights

ALTERNATIVE SERVICES:
- Vast.ai: $0.70-1.20/hour (community marketplace)
- Lambda Labs: $1.10/hour
- Google Colab Pro+: $50/month (limited)
"""
        text.insert(tk.END, guide_content)
        text.config(state=tk.DISABLED)
        
    def start_installation(self):
        """Begin installation process"""
        # Get selected models
        selected = [key for key, var in self.selected_models.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("No Models Selected", "Please select at least one model to install.")
            return
            
        mode = self.install_mode.get()
        
        if mode == "cloud":
            self.log("🌐 Cloud Mode Selected")
            self.log("⚠️ Please follow the Cloud Setup Guide to create your GPU instance first.")
            self.log("Then run this installer on your cloud instance.")
            self.show_cloud_guide()
            return
            
        # Confirm installation
        total_vram = sum(int(self.models[m]['vram'].replace('GB', '').replace('+', '')) 
                        for m in selected if self.models[m]['vram'] != "60GB+")
        
        confirm = messagebox.askyesno(
            "Confirm Installation",
            f"Install {len(selected)} model(s):\n" +
            "\n".join(f"- {self.models[m]['name']}" for m in selected) +
            f"\n\nEstimated VRAM needed: ~{total_vram}GB" +
            "\n\nContinue?"
        )
        
        if not confirm:
            return
            
        self.install_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        try:
            self.run_installation(selected, mode)
        except Exception as e:
            self.log(f"❌ Installation failed: {e}")
            messagebox.showerror("Installation Error", str(e))
        finally:
            self.progress.stop()
            self.install_btn.config(state=tk.NORMAL)
            
    def run_installation(self, models: List[str], mode: str):
        """Execute installation steps"""
        self.log("=" * 60)
        self.log("🚀 Starting Hunyuan Installation")
        self.log("=" * 60)
        
        install_path = Path(self.dir_entry.get())
        install_path.mkdir(parents=True, exist_ok=True)
        
        self.log(f"📁 Installation directory: {install_path}")
        self.log(f"📦 Mode: {mode}")
        self.log(f"📋 Models to install: {', '.join(models)}")
        self.log("")
        
        for i, model_key in enumerate(models, 1):
            model = self.models[model_key]
            self.log(f"[{i}/{len(models)}] Installing {model['name']}...")
            self.log(f"  Repository: {model['repo']}")
            
            # Clone repository
            repo_path = install_path / model_key
            if repo_path.exists():
                self.log(f"  ⚠️ Directory exists, skipping clone: {repo_path}")
            else:
                self.log(f"  📥 Cloning repository...")
                try:
                    result = subprocess.run(
                        ["git", "clone", model['repo'], str(repo_path)],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    if result.returncode == 0:
                        self.log(f"  ✅ Clone successful")
                    else:
                        self.log(f"  ❌ Clone failed: {result.stderr}")
                        continue
                except Exception as e:
                    self.log(f"  ❌ Clone error: {e}")
                    continue
            
            if mode != "deps":
                self.log(f"  ℹ️ Model weights need to be downloaded separately")
                self.log(f"  See README in {repo_path}")
            
            self.log("")
        
        self.log("=" * 60)
        self.log("✅ Installation Complete!")
        self.log("=" * 60)
        self.log("")
        self.log("Next steps:")
        self.log("1. Download model weights for each installed model")
        self.log("2. Set up conda/python environments")
        self.log("3. Install dependencies (requirements.txt in each folder)")
        self.log("4. See individual README files for specific instructions")
        
        messagebox.showinfo("Installation Complete", 
                          "Installation finished! Check the log for details.")

def main():
    root = tk.Tk()
    app = HunyuanInstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

