# RunPod Setup Guide for Hunyuan Models

Complete guide to setting up and using RunPod for Hunyuan AI models.

## 🌐 What is RunPod?

RunPod is a cloud GPU rental service that provides access to powerful GPUs on-demand. It's perfect for running Hunyuan models without buying expensive hardware.

## 💰 Pricing (as of 2025)

| GPU Type | VRAM | On-Demand | Spot (Interruptible) |
|----------|------|-----------|---------------------|
| A100 80GB PCIe | 80GB | $1.64/hour | $0.82/hour |
| A100 80GB SXM | 80GB | $1.74/hour | $0.87/hour |
| H100 80GB PCIe | 80GB | $2.15/hour | $1.08/hour |
| A40 | 48GB | $0.40/hour | $0.20/hour |

**Storage:** ~$0.10/GB/month for persistent volumes

## 📋 Step-by-Step Setup

### 1. Create RunPod Account

1. Go to https://runpod.io/
2. Click "Sign Up" in the top right
3. Create account with email or GitHub
4. Verify your email address

### 2. Add Credits

1. Click your profile icon > "Billing"
2. Add credits via:
   - Credit/Debit card
   - Crypto
3. **Recommended starting amount:** $20-50
   - This gives you 10-25 hours on A100 80GB

### 3. Deploy Your GPU Instance

1. **Click "Deploy" in top menu**
   
2. **Select "GPU Cloud"**

3. **Choose GPU Type:**
   - For full Hunyuan suite: **A100 80GB**
   - For 3D/Image models only: A40 48GB (cheaper)
   - Filter: Click "80GB" under VRAM

4. **Select Template:**
   - Recommended: **"PyTorch 2.0"** or **"RunPod PyTorch"**
   - These come with CUDA pre-installed
   - Alternative: "RunPod Stable Diffusion" (has ML tools)

5. **Configure Storage:**
   - Container Disk: 50GB (minimum)
   - Volume Disk: 200GB+ (recommended)
   - ✅ Check "Use Volume" for persistent storage

6. **Choose Instance Type:**
   - **On-Demand:** Guaranteed availability, higher cost
   - **Spot:** Cheaper but can be interrupted
   - *For experimentation:* Start with Spot
   - *For production:* Use On-Demand

7. **Click "Deploy On-Demand" or "Deploy Spot"**

### 4. Connect to Your Instance

Your pod will start in 2-3 minutes.

#### Option A: JupyterLab (Easiest)

1. Click "Connect" button on your pod
2. Click "Start Jupyter Lab"
3. Wait for JupyterLab to load
4. Click "Terminal" icon to open terminal

#### Option B: SSH (Advanced)

1. Add your SSH public key in RunPod settings first
2. Click "Connect" > "SSH over exposed TCP"
3. Copy the SSH command
4. Run in your local terminal:
   ```bash
   ssh -p [PORT] root@[IP]
   ```

### 5. Setup Hunyuan Environment

In the terminal (JupyterLab or SSH):

```bash
# Update system
apt update && apt upgrade -y

# Install git if needed
apt install git -y

# Clone the quickstart installer
cd /workspace
git clone https://github.com/YOUR_USERNAME/hunyuan-quickstart.git
cd hunyuan-quickstart

# Run the automated setup
chmod +x cloud_setup/setup_cloud.sh
./cloud_setup/setup_cloud.sh
```

Or use the GUI installer:
```bash
python3 installer_gui.py
```

### 6. Download Model Weights

Each Hunyuan model requires downloading large weight files:

```bash
# Example for HunyuanVideo-I2V
cd /workspace/HunyuanVideo-I2V
# Follow instructions in ckpts/README.md
```

**Tip:** Use Hugging Face CLI for faster downloads:
```bash
pip install huggingface-hub
huggingface-cli login
# Enter your HF token
```

### 7. Run Your First Generation

```bash
cd /workspace/HunyuanVideo-I2V
python3 sample_image2video.py \
    --model HYVideo-T/2 \
    --prompt "A beautiful sunset over the ocean" \
    --i2v-mode \
    --i2v-image-path ./assets/demo/i2v/imgs/0.jpg \
    --i2v-resolution 720p \
    --video-length 129 \
    --flow-reverse \
    --seed 0 \
    --save-path ./results
```

## 💡 Cost-Saving Tips

### 1. Stop Pod When Not Using
- Click "Stop" button when done
- You only pay for storage (~$0.10/GB/month)
- Restart anytime by clicking "Start"

### 2. Use Spot Instances
- 30-40% cheaper than On-Demand
- Good for experimentation
- Can be interrupted (rare)

### 3. Use Persistent Volumes
- Store model weights on volume
- Don't re-download each time
- Attach volume to new pods

### 4. Download Results Immediately
```bash
# In JupyterLab, right-click file > Download
# Or use SCP:
scp -P [PORT] root@[IP]:/workspace/results/*.mp4 ./local_folder/
```

### 5. Set Budget Alerts
- RunPod Settings > Billing > Notifications
- Set alert when credits drop below threshold

### 6. Terminate (Not Stop) When Done Long-Term
- "Terminate" deletes container (keeps volume)
- "Stop" keeps container (charges storage)
- Terminate saves more money if not using for days

## 📊 Example Cost Calculations

### Scenario 1: Casual User
- 5 hours/week video generation
- A100 80GB PCIe Spot: $0.82/hour
- **Weekly cost:** $4.10
- **Monthly cost:** ~$16

### Scenario 2: Heavy User
- 20 hours/week
- A100 80GB PCIe On-Demand: $1.64/hour
- **Weekly cost:** $32.80
- **Monthly cost:** ~$131

### Scenario 3: Project Work
- 40 hours total for a project
- A100 80GB PCIe Spot: $0.82/hour
- **Total cost:** $32.80

**Compare to buying A100 80GB:** $10,000-15,000

## 🔧 Troubleshooting

### Pod Won't Start
- Try different region/data center
- Check if credits are sufficient
- Wait a few minutes (high demand)

### Conda Issues
- **"conda: command not found"**: Restart terminal or run `source ~/.bashrc`
- **Terms of Service error**: Run these commands:
  ```bash
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
  ```
- **Environment activation issues**: Use `eval "$(conda shell.bash hook)"` before activating

### Out of Memory Error
- Close other applications
- Reduce video resolution
- Use `--use-cpu-offload` flag

### Slow Downloads
- Use tmux to keep downloads running:
  ```bash
  apt install tmux
  tmux new -s download
  # Run download command
  # Press Ctrl+B, then D to detach
  ```

### Can't Access JupyterLab
- Try SSH option instead
- Check firewall settings
- Restart pod

### Setup Script Issues
- If conda installation fails, restart terminal and run script again
- For permission errors, ensure you're running as root or with sudo

## 📁 Recommended Directory Structure

```
/workspace/
├── hunyuan-quickstart/          # This installer
├── HunyuanVideo/                # Video models
├── HunyuanVideo-I2V/
├── Hunyuan3D/
├── models/                      # Shared model weights
│   └── checkpoints/
└── results/                     # Your generated content
    ├── videos/
    └── images/
```

## 🔗 Useful Links

- RunPod Dashboard: https://www.runpod.io/console/pods
- RunPod Documentation: https://docs.runpod.io/
- RunPod Community Discord: https://discord.gg/pJ3P2DbUUq
- HunyuanVideo Docs: https://github.com/Tencent-Hunyuan/HunyuanVideo

## 🆘 Getting Help

1. **RunPod Issues:** RunPod Discord or support ticket
2. **Hunyuan Issues:** GitHub Issues on respective repos
3. **This Installer:** Open issue on hunyuan-quickstart repo

## ⚡ Quick Reference Commands

```bash
# Check GPU
nvidia-smi

# Monitor GPU usage in real-time
watch -n 1 nvidia-smi

# Check disk space
df -h

# Find large files
du -h --max-depth=1 | sort -hr

# Download results via Python
python3 -m http.server 8000
# Then access via browser: http://[POD-IP]:8000

# Keep process running after disconnect
tmux new -s hunyuan
# Run your command
# Detach: Ctrl+B, then D
# Reattach: tmux attach -t hunyuan
```

---

**Ready to start?** Go to https://runpod.io/ and deploy your first pod! 🚀

