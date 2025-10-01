# 🚀 Hunyuan Quickstart Guide

Get started with Hunyuan AI models in minutes!

## ⚡ Super Quick Start

### Windows
```bash
# Just double-click:
hunyuan-installer.bat
```

### Linux / WSL2
```bash
chmod +x hunyuan-installer.sh
./hunyuan-installer.sh
```

## 🌐 Cloud GPU Setup (Recommended)

### Why Cloud GPU?
- ✅ No expensive hardware needed
- ✅ Pay only for what you use (~$2/hour)
- ✅ Access to 80GB A100 GPUs
- ✅ Start generating in minutes

### RunPod Setup (5 minutes)

1. **Create account:** https://runpod.io/
2. **Add $20-50 credits**
3. **Deploy GPU:**
   - Select: A100 80GB
   - Template: PyTorch 2.0
   - Storage: 200GB
4. **Connect via JupyterLab**
5. **Run in terminal:**
   ```bash
   cd /workspace
   git clone [YOUR_REPO_URL]
   cd hunyuan-quickstart
   ./cloud_setup/setup_cloud.sh
   ```

**Full guide:** See `cloud_setup/runpod_guide.md`

## 💻 Local Installation

### Requirements
- 60-80GB GPU VRAM (A100/H100)
- Linux or WSL2
- 200GB+ free disk space
- CUDA 12.4 or 11.8

### Steps
1. Run installer:
   ```bash
   python3 installer_gui.py
   ```
2. Select "Local Installation"
3. Choose models to install
4. Follow prompts

## 📋 What Gets Installed

### Video Models (60GB VRAM each)
- **HunyuanVideo** - Text-to-video generation
- **HunyuanVideo-I2V** - Image-to-video generation

### 3D Models (20-60GB VRAM)
- **HunyuanWorld** - 3D world generation
- **Hunyuan3D** - 3D object generation

### Image Models (20GB VRAM)
- **HunyuanDiT** - High-quality image generation

## 🎯 After Installation

### Download Model Weights
Each model needs weights downloaded separately:

```bash
# Login to Hugging Face
huggingface-cli login

# Download weights (example)
cd HunyuanVideo-I2V
# Follow ckpts/README.md instructions
```

### Create Environment
```bash
# Create conda environment
conda create -n hunyuan python==3.11.9
conda activate hunyuan

# Install dependencies
cd HunyuanVideo-I2V
pip install -r requirements.txt
```

### Generate Your First Video
```bash
python sample_image2video.py \
    --model HYVideo-T/2 \
    --prompt "A beautiful sunset over the ocean" \
    --i2v-mode \
    --i2v-image-path ./assets/demo/i2v/imgs/0.jpg \
    --i2v-resolution 720p \
    --video-length 129 \
    --flow-reverse \
    --seed 0
```

## 💰 Cost Comparison

### Cloud GPU (RunPod A100 80GB)
- **Setup cost:** $0
- **Usage:** $1.89/hour on-demand, $1.29/hour spot
- **10 hours/month:** ~$19
- **Best for:** Occasional use, experimentation

### Buy GPU (A100 80GB)
- **Hardware:** $10,000-15,000
- **Electricity:** ~$50-100/month
- **Best for:** Daily heavy use, production

## 🆘 Troubleshooting

### "No GPU detected"
- Check: `nvidia-smi`
- Install NVIDIA drivers
- On WSL2: Install CUDA on WSL

### "Out of memory"
- Use smaller resolution
- Enable CPU offload: `--use-cpu-offload`
- Close other applications

### "Model weights not found"
- Download weights first (see model README)
- Check paths in config

## 📚 Learn More

- [Full RunPod Guide](cloud_setup/runpod_guide.md)
- [HunyuanVideo-I2V Docs](https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V)
- [HunyuanVideo Docs](https://github.com/Tencent-Hunyuan/HunyuanVideo)

## 🤝 Contributing

Found a bug? Have a suggestion? Open an issue or PR!

## 📄 License

MIT License - See LICENSE file

Individual Hunyuan models have their own licenses.

---

**Ready to create amazing AI videos?** Start with the cloud setup above! 🎥✨

