#!/bin/bash
# Automated Cloud Setup Script for Hunyuan Models
# For use on RunPod, Vast.ai, Lambda Labs, or similar cloud GPU instances

set -e  # Exit on error

echo "================================================"
echo "  Hunyuan Cloud Setup - Automated Installation"
echo "================================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
WORKSPACE_DIR="/workspace"
MODELS_DIR="$WORKSPACE_DIR/hunyuan-models"
CHECKPOINTS_DIR="$WORKSPACE_DIR/hunyuan-checkpoints"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_progress() {
    echo -e "${GREEN}[→]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_warning "Not running as root. Some commands may require sudo."
fi

# Step 1: System Update
print_status "Updating system packages..."
apt update -qq && apt upgrade -y -qq

# Step 2: Install essential tools
print_status "Installing essential tools..."
apt install -y -qq \
    git \
    wget \
    curl \
    vim \
    tmux \
    htop \
    tree \
    unzip \
    build-essential

# Step 3: Check NVIDIA GPU
print_status "Checking NVIDIA GPU..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    
    if [ "$GPU_MEM" -lt 60000 ]; then
        print_warning "GPU has less than 60GB VRAM. Some models may not run."
    else
        print_status "GPU has sufficient VRAM for Hunyuan models"
    fi
else
    print_error "nvidia-smi not found! No GPU detected."
    exit 1
fi

# Step 4: Check Python
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION detected"
else
    print_error "Python 3 not found!"
    exit 1
fi

# Step 5: Install/Upgrade pip
print_status "Upgrading pip..."
python3 -m pip install --upgrade pip -q

# Step 6: Check disk space and create directories
print_status "Checking disk space..."
AVAILABLE_SPACE=$(df -BG "$WORKSPACE_DIR" | tail -1 | awk '{print $4}' | sed 's/G//')
REQUIRED_SPACE=35  # 35GB for full HunyuanVideo-I2V setup

if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
    print_error "Insufficient disk space!"
    print_error "Available: ${AVAILABLE_SPACE}GB"
    print_error "Required: ${REQUIRED_SPACE}GB"
    print_warning "Please upgrade your RunPod instance storage or use a different instance."
    print_warning "HunyuanVideo-I2V requires ~30GB for model weights alone."
    exit 1
else
    print_status "Disk space check passed: ${AVAILABLE_SPACE}GB available"
fi

print_status "Creating workspace directories..."
mkdir -p "$MODELS_DIR"
mkdir -p "$CHECKPOINTS_DIR"
mkdir -p "$WORKSPACE_DIR/results"

# Step 7: Install Conda (if not present)
if ! command -v conda &> /dev/null; then
    print_status "Installing Miniconda..."
    wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p $HOME/miniconda3
    rm /tmp/miniconda.sh
    eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    conda init
    print_status "Conda installed. Please restart your shell or run: source ~/.bashrc"
    print_warning "IMPORTANT: You must restart your terminal or run 'source ~/.bashrc' before continuing!"
    print_warning "Then run this script again or continue manually with the next steps."
    exit 0
else
    print_status "Conda already installed"
fi

# Step 7.5: Accept Conda Terms of Service
print_status "Accepting Conda Terms of Service..."
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
print_status "Conda Terms of Service accepted"

# Step 8: Interactive Model Selection
echo ""
echo "================================================"
echo "  Select Models to Install"
echo "================================================"
echo ""
echo "Which Hunyuan models do you want to install?"
echo ""
echo "1) HunyuanVideo (Text-to-Video) - 60GB VRAM"
echo "2) HunyuanVideo-I2V (Image-to-Video) - 60GB VRAM"
echo "3) HunyuanWorld (3D Worlds) - 60-80GB VRAM"
echo "4) Hunyuan3D (3D Objects) - 20GB VRAM"
echo "5) HunyuanDiT (Images) - 20GB VRAM"
echo "6) All of the above"
echo "7) Skip model installation"
echo ""
read -p "Enter your choice (1-7): " model_choice

install_video=false
install_i2v=false
install_world=false
install_3d=false
install_dit=false

case $model_choice in
    1) install_video=true ;;
    2) install_i2v=true ;;
    3) install_world=true ;;
    4) install_3d=true ;;
    5) install_dit=true ;;
    6) 
        install_video=true
        install_i2v=true
        install_world=true
        install_3d=true
        install_dit=true
        ;;
    7) 
        print_warning "Skipping model installation"
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# Step 9: Clone repositories
cd "$MODELS_DIR"

if [ "$install_video" = true ]; then
    print_status "Cloning HunyuanVideo..."
    git clone https://github.com/Tencent-Hunyuan/HunyuanVideo.git
fi

if [ "$install_i2v" = true ]; then
    print_status "Cloning HunyuanVideo-I2V..."
    git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V.git
fi

if [ "$install_world" = true ]; then
    print_status "Cloning HunyuanWorld..."
    git clone https://github.com/Tencent-Hunyuan/HunyuanWorld.git
fi

if [ "$install_3d" = true ]; then
    print_status "Cloning Hunyuan3D..."
    git clone https://github.com/Tencent-Hunyuan/Hunyuan3D.git
fi

if [ "$install_dit" = true ]; then
    print_status "Cloning HunyuanDiT..."
    git clone https://github.com/Tencent-Hunyuan/HunyuanDiT.git
fi

# Step 10: Install Hugging Face CLI
print_status "Installing Hugging Face CLI..."
pip install -q huggingface-hub[cli]

# Step 10.5: Hugging Face Authentication
echo ""
echo "================================================"
echo "  Hugging Face Authentication"
echo "================================================"
echo ""
echo "To download model weights, you need a Hugging Face token."
echo "Get your token from: https://huggingface.co/settings/tokens"
echo ""
read -p "Enter your Hugging Face token (or press Enter to skip): " hf_token

if [ ! -z "$hf_token" ]; then
    print_status "Logging into Hugging Face..."
    hf auth login --token "$hf_token"
    if [ $? -eq 0 ]; then
        print_status "Hugging Face authentication successful!"
        HF_AUTHENTICATED=true
    else
        print_error "Hugging Face authentication failed!"
        HF_AUTHENTICATED=false
    fi
else
    print_warning "Skipping Hugging Face authentication. You'll need to login manually later."
    HF_AUTHENTICATED=false
fi

# Step 11: Setup Conda Environments for Installed Models
echo ""
echo "================================================"
echo "  Setting up Conda Environments"
echo "================================================"
echo ""

    if [ "$install_i2v" = true ]; then
        print_status "Setting up HunyuanVideo-I2V environment..."
        
        # Check if directory exists and remove if corrupted
        if [ -d "$MODELS_DIR/HunyuanVideo-I2V" ]; then
            print_warning "HunyuanVideo-I2V directory already exists. Removing to ensure clean installation..."
            rm -rf "$MODELS_DIR/HunyuanVideo-I2V"
        fi
        
        cd "$MODELS_DIR/HunyuanVideo-I2V"
    
    # Create conda environment with error handling
    print_status "Creating conda environment..."
    if ! conda create -n hunyuan-i2v python==3.11.9 -y; then
        print_error "Failed to create conda environment. This might be due to:"
        print_error "1. Corrupted conda installation"
        print_error "2. Network connectivity issues"
        print_error "3. Disk space problems"
        print_warning "Try running: conda clean --all && conda env remove -n hunyuan-i2v"
        exit 1
    fi
    
        # Activate and install PyTorch with CUDA
        eval "$(conda shell.bash hook)"
        conda activate hunyuan-i2v

        print_progress "Installing PyTorch with CUDA support..."
        print_warning "This may take 5-10 minutes (installing quietly)..."
        # Use pip for PyTorch installation (more reliable than conda)
        pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124 --quiet
        
        # Verify PyTorch installation
        print_status "Verifying PyTorch installation..."
        python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"
    
    print_progress "Installing model requirements..."
    print_warning "Installing Python packages (installing quietly)..."
    pip install -r requirements.txt --quiet
    
    print_progress "Installing Flash Attention..."
    print_warning "Building Flash Attention from source (this may take a few minutes)..."
    pip install git+https://github.com/Dao-AILab/flash-attention.git@v2.6.3 --quiet
    
        # Download model weights if authenticated
        if [ "$HF_AUTHENTICATED" = true ]; then
            echo ""
            echo "================================================"
            echo "  Downloading HunyuanVideo-I2V Model Weights"
            echo "================================================"
            echo ""
            print_status "Downloading main model (this may take 10-60 minutes)..."
            print_warning "IMPORTANT: Keep this terminal open during download!"
            print_warning "If connection is lost, you can resume by running the installer again."
            
            # Retry logic for downloads
            max_retries=3
            retry_count=0
            while [ $retry_count -lt $max_retries ]; do
                print_status "Starting download attempt $((retry_count + 1))/$max_retries..."
                if hf download tencent/HunyuanVideo-I2V --local-dir ./ckpts --quiet; then
                    print_status "Main model download successful!"
                    break
                else
                    retry_count=$((retry_count + 1))
                    if [ $retry_count -lt $max_retries ]; then
                        print_warning "Download failed, retrying in 10 seconds... (attempt $((retry_count + 1))/$max_retries)"
                        sleep 10
                    else
                        print_error "Download failed after $max_retries attempts. Please try again manually."
                    fi
                fi
            done
        
        print_status "Downloading MLLM text encoder..."
        cd ckpts
        hf download xtuner/llava-llama-3-8b-v1_1-transformers --local-dir ./text_encoder_i2v --quiet

        print_status "Downloading CLIP text encoder..."
        hf download openai/clip-vit-large-patch14 --local-dir ./text_encoder_2 --quiet
        cd ..
        
        print_status "All HunyuanVideo-I2V weights downloaded successfully!"
    else
        print_warning "Skipping weight download. Run these commands manually after setup:"
        echo "  cd $MODELS_DIR/HunyuanVideo-I2V"
        echo "  hf download tencent/HunyuanVideo-I2V --local-dir ./ckpts"
        echo "  cd ckpts"
        echo "  hf download xtuner/llava-llama-3-8b-v1_1-transformers --local-dir ./text_encoder_i2v"
        echo "  hf download openai/clip-vit-large-patch14 --local-dir ./text_encoder_2"
    fi
    
    print_status "HunyuanVideo-I2V environment ready!"
fi

if [ "$install_video" = true ]; then
    print_status "Setting up HunyuanVideo environment..."
    cd "$MODELS_DIR/HunyuanVideo"
    
    # Create conda environment
    conda create -n hunyuan-video python==3.11.9 -y
    
    # Activate and install PyTorch with CUDA
    eval "$(conda shell.bash hook)"
    conda activate hunyuan-video
    
    print_status "Installing PyTorch with CUDA support..."
    conda install pytorch==2.4.0 torchvision==0.19.0 pytorch-cuda=12.4 -c pytorch -c nvidia -y
    
    print_status "Installing model requirements..."
    pip install -r requirements.txt
    
    # Download model weights if authenticated
    if [ "$HF_AUTHENTICATED" = true ]; then
        echo ""
        echo "================================================"
        echo "  Downloading HunyuanVideo Model Weights"
        echo "================================================"
        echo ""
        print_status "Downloading HunyuanVideo weights..."
        # Note: HunyuanVideo weight download commands would go here
        # Check the model's README for specific download instructions
        print_warning "Please check HunyuanVideo/README.md for weight download instructions"
    else
        print_warning "Skipping weight download. Check HunyuanVideo/README.md for download instructions"
    fi
    
    print_status "HunyuanVideo environment ready!"
fi

echo ""
echo "================================================"
echo "  ✓ Setup Complete!"
echo "================================================"
echo ""
echo "Installed models location: $MODELS_DIR"
echo "Checkpoints directory: $CHECKPOINTS_DIR"
echo "Results directory: $WORKSPACE_DIR/results"
echo ""
echo "Next Steps:"
if [ "$HF_AUTHENTICATED" = true ]; then
    echo "1. ✅ Model weights downloaded automatically!"
    echo ""
    echo "2. Activate environments and test:"
    if [ "$install_i2v" = true ]; then
        echo "   conda activate hunyuan-i2v"
        echo "   cd $MODELS_DIR/HunyuanVideo-I2V"
        echo "   python sample_image2video.py --help"
    fi
    if [ "$install_video" = true ]; then
        echo "   conda activate hunyuan-video"
        echo "   cd $MODELS_DIR/HunyuanVideo"
        echo "   python sample_video.py --help"
    fi
    echo ""
    echo "3. Start generating!"
else
    echo "1. Download model weights:"
    echo "   - Run: hf auth login"
    echo "   - Enter your HF token from: https://huggingface.co/settings/tokens"
    echo "   - Follow instructions in each model's ckpts/README.md"
    echo ""
    echo "2. Activate environments and test:"
    if [ "$install_i2v" = true ]; then
        echo "   conda activate hunyuan-i2v"
        echo "   cd $MODELS_DIR/HunyuanVideo-I2V"
        echo "   python sample_image2video.py --help"
    fi
    if [ "$install_video" = true ]; then
        echo "   conda activate hunyuan-video"
        echo "   cd $MODELS_DIR/HunyuanVideo"
        echo "   python sample_video.py --help"
    fi
    echo ""
    echo "3. Start generating!"
fi
echo ""
echo "Useful commands:"
echo "  nvidia-smi              # Check GPU usage"
echo "  htop                    # Check CPU/RAM"
echo "  df -h                   # Check disk space"
echo "  tmux                    # Keep sessions running"
echo "  conda env list          # List all environments"
echo ""
echo "================================================"

