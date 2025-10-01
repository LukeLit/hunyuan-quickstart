# Hunyuan Quickstart Installer

A GUI-based installer for setting up the complete Tencent Hunyuan AI suite on cloud GPUs or local systems.

## Supported Models

- **HunyuanVideo** - Text-to-Video generation
- **HunyuanVideo-I2V** - Image-to-Video generation  
- **HunyuanWorld** - 3D World generation
- **Hunyuan3D** - 3D Object generation
- **HunyuanImage** - Image generation
- **HunyuanDiT** - Diffusion Image generation

## Features

- ✅ Interactive GUI for selecting which models to install
- ✅ Automated dependency installation
- ✅ RunPod cloud GPU setup guide
- ✅ Model weight downloading with progress tracking
- ✅ Environment configuration
- ✅ WSL2 and native Linux support
- ✅ Quick launch scripts for each model

## Quick Start

### Windows
```bash
# Double-click or run:
hunyuan-installer.bat
```

### Linux / WSL2
```bash
chmod +x hunyuan-installer.sh
./hunyuan-installer.sh
```

### Python GUI
```bash
python installer_gui.py
```

## System Requirements

### Local Installation
- **Minimum:** 60GB GPU VRAM (RTX 3090 or better for smaller models)
- **Recommended:** 80GB GPU VRAM (A100 80GB for full suite)
- **OS:** Linux, WSL2, or Windows with Docker
- **CUDA:** 12.4 or 11.8+

### Cloud GPU (Recommended)
- RunPod, Vast.ai, Lambda Labs, or similar
- A100 80GB instance
- Cost: ~$1-3/hour

## Installation Options

1. **Quick Install (All Models)** - Installs everything
2. **Custom Install** - Choose specific models
3. **Cloud Setup** - Instructions for RunPod/cloud GPUs
4. **Dependencies Only** - Just Python environment

## Project Structure

```
hunyuan-quickstart/
├── installer_gui.py          # Main GUI installer
├── hunyuan-installer.bat     # Windows launcher
├── hunyuan-installer.sh      # Linux launcher  
├── cloud_setup/
│   ├── runpod_guide.md      # RunPod setup instructions
│   └── setup_cloud.sh       # Cloud instance setup script
├── installers/
│   ├── base_installer.py    # Core installation logic
│   ├── video_installer.py   # Video models
│   ├── image_installer.py   # Image models
│   └── world_installer.py   # 3D/World models
└── launch_scripts/
    ├── launch_video.bat
    ├── launch_i2v.bat
    └── ...
```

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## License

This installer is provided as-is. Individual Hunyuan models have their own licenses.

## Support

For issues or questions, please open an issue on GitHub.

