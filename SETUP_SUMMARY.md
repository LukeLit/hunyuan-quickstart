# 🎉 Hunyuan Quickstart Repository - Setup Complete!

## ✅ What We've Built

You now have a professional quickstart repository for the entire Hunyuan AI suite!

### 📁 Repository Structure

```
hunyuan-quickstart/
│
├── 📄 README.md                    # Full documentation
├── 📄 QUICKSTART.md                # Quick start guide
├── 📄 LICENSE                      # MIT License
├── 📄 .gitignore                   # Git ignore rules
│
├── 🖥️ installer_gui.py             # Interactive GUI installer
├── 🪟 hunyuan-installer.bat        # Windows launcher
├── 🐧 hunyuan-installer.sh         # Linux/WSL2 launcher
│
└── cloud_setup/
    ├── 📖 runpod_guide.md          # Complete RunPod tutorial
    └── 🔧 setup_cloud.sh           # Automated cloud setup script
```

## 🎯 Features

### ✨ Interactive GUI
- Select which Hunyuan models to install
- Choose installation mode (cloud/local/dependencies only)
- System information checker
- Built-in cloud setup guide
- Real-time installation logging

### 🌐 Cloud GPU Support
- Complete RunPod setup guide
- Cost calculators
- Troubleshooting tips
- Automated setup script

### 🚀 Easy Launch
- Windows: Double-click `hunyuan-installer.bat`
- Linux/WSL2: Run `./hunyuan-installer.sh`
- Python: `python installer_gui.py`

## 📊 Supported Models

| Model | Purpose | Min VRAM | Status |
|-------|---------|----------|--------|
| HunyuanVideo | Text-to-Video | 60GB | ✅ Ready |
| HunyuanVideo-I2V | Image-to-Video | 60GB | ✅ Ready |
| HunyuanWorld | 3D Worlds | 60-80GB | ✅ Ready |
| Hunyuan3D | 3D Objects | 20GB | ✅ Ready |
| HunyuanDiT | Images | 20GB | ✅ Ready |

## 🔄 Next Steps

### 1. Test the Installer Locally (Optional)

You can test the GUI on your Windows machine:

```bash
cd D:\Hunyuan\hunyuan-quickstart
python installer_gui.py
```

This will let you see the interface and options before using it on cloud GPU.

### 2. Push to GitHub

Create a new repository on GitHub, then:

```bash
cd D:\Hunyuan\hunyuan-quickstart
git remote add origin https://github.com/YOUR_USERNAME/hunyuan-quickstart.git
git branch -M main
git push -u origin main
```

### 3. Set Up RunPod

Follow these steps to get your cloud GPU ready:

#### A. Create RunPod Account
1. Go to https://runpod.io/
2. Sign up with email or GitHub
3. Add credits ($20-50 recommended to start)

#### B. Deploy GPU Instance
1. Click "Deploy" > "GPU Cloud"
2. **Filter for:** 80GB VRAM
3. **Select:** A100 80GB
4. **Template:** PyTorch 2.0
5. **Storage:** 
   - Container Disk: 50GB
   - Volume Disk: 200GB+ (check "Use Volume")
6. **Type:** Start with "Spot" (cheaper) or "On-Demand" (guaranteed)
7. Click "Deploy"

#### C. Connect & Setup
1. Wait 2-3 minutes for pod to start
2. Click "Connect" > "Start Jupyter Lab"
3. In JupyterLab, click "Terminal"
4. Run:

```bash
# Clone your repository
cd /workspace
git clone https://github.com/YOUR_USERNAME/hunyuan-quickstart.git
cd hunyuan-quickstart

# Run automated setup
chmod +x cloud_setup/setup_cloud.sh
./cloud_setup/setup_cloud.sh
```

5. Follow the prompts to select which models to install

### 4. Download Model Weights

After setup, download the weights for your chosen models:

```bash
# Login to Hugging Face (one time)
pip install huggingface-hub
huggingface-cli login
# Enter token from: https://huggingface.co/settings/tokens

# Download weights (example for I2V)
cd /workspace/hunyuan-models/HunyuanVideo-I2V
# Follow instructions in ckpts/README.md
```

### 5. Create Conda Environment & Install Dependencies

```bash
# Create environment
conda create -n hunyuan-i2v python==3.11.9
conda activate hunyuan-i2v

# Install PyTorch
conda install pytorch==2.4.0 torchvision==0.19.0 pytorch-cuda=12.4 -c pytorch -c nvidia

# Install dependencies
cd /workspace/hunyuan-models/HunyuanVideo-I2V
pip install -r requirements.txt
pip install git+https://github.com/Dao-AILab/flash-attention.git@v2.6.3
```

### 6. Generate Your First Video! 🎬

```bash
cd /workspace/hunyuan-models/HunyuanVideo-I2V

python3 sample_image2video.py \
    --model HYVideo-T/2 \
    --prompt "An Asian man waves a firework stick." \
    --i2v-mode \
    --i2v-image-path ./assets/demo/i2v/imgs/0.jpg \
    --i2v-resolution 720p \
    --i2v-stability \
    --infer-steps 50 \
    --video-length 129 \
    --flow-reverse \
    --flow-shift 7.0 \
    --seed 0 \
    --embedded-cfg-scale 6.0 \
    --save-path ./results
```

### 7. Download Results

In JupyterLab:
- Navigate to `/workspace/results/`
- Right-click the video file
- Select "Download"

## 💰 Cost Management

### Estimated Costs (A100 80GB)
- **On-Demand:** $1.89/hour
- **Spot:** $1.29/hour
- **Storage:** ~$0.10/GB/month

### Cost-Saving Tips
✅ **Stop pod when not using** (only pay for storage)
✅ **Use Spot instances** for testing (30% cheaper)
✅ **Set budget alerts** in RunPod settings
✅ **Download results immediately**
✅ **Use persistent volumes** (don't re-download weights)

### Example Monthly Costs
- **Light use** (5 hrs/week): ~$26/month
- **Medium use** (10 hrs/week): ~$52/month
- **Heavy use** (20 hrs/week): ~$103/month

Compare to buying A100 80GB: **$10,000-15,000** 💸

## 🤝 Share with Team

### For Your Teammates

Send them:
1. **GitHub repo link**: `https://github.com/YOUR_USERNAME/hunyuan-quickstart`
2. **Quick instructions**:
   ```
   Hey team! I've set up a quickstart repo for Hunyuan AI models.

   To get started:
   1. Create RunPod account: https://runpod.io/
   2. Deploy A100 80GB GPU (see guide in repo)
   3. Run the automated installer
   4. Start creating!

   Full guide: [your repo]/blob/main/QUICKSTART.md
   RunPod tutorial: [your repo]/blob/main/cloud_setup/runpod_guide.md
   ```

### Team Benefits
- ✅ Consistent setup across team
- ✅ No manual dependency configuration
- ✅ Automated model installation
- ✅ Comprehensive documentation
- ✅ Cost tracking guidance

## 📚 Documentation Links

- **This Repo:** Will be at `https://github.com/YOUR_USERNAME/hunyuan-quickstart`
- **HunyuanVideo-I2V:** https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V
- **HunyuanVideo:** https://github.com/Tencent-Hunyuan/HunyuanVideo
- **Hunyuan3D:** https://github.com/Tencent-Hunyuan/Hunyuan3D
- **RunPod Docs:** https://docs.runpod.io/

## 🆘 Support

### Issues with Installer
- Open issue on your repo

### Issues with Hunyuan Models
- Check official repo GitHub issues

### Issues with RunPod
- RunPod Discord: https://discord.gg/pJ3P2DbUUq
- Support ticket

## 🎊 You're All Set!

Your quickstart repository is ready to make Hunyuan AI accessible to your entire team!

**Next:** Push to GitHub and set up your first RunPod instance! 🚀

---

**Questions?** Open an issue or refer to the guides in the repo.

**Happy generating!** 🎥✨🎨

