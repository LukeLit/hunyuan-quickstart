# 🌐 HunyuanVideo-I2V Web API

A beautiful web interface and REST API for HunyuanVideo-I2V image-to-video generation.

## 🚀 Quick Start

### 1. Start the Web Server

```bash
# Activate the HunyuanVideo-I2V environment
conda activate hunyuan-i2v

# Navigate to web API directory
cd /workspace/hunyuan-quickstart/web_api

# Install web dependencies
pip install -r requirements.txt

# Start the server
python start_server.py
```

### 2. Access the Web Interface

Open your browser and go to:
- **Web Interface**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## 🎯 Features

### Web Interface
- ✅ **Drag & Drop Image Upload**
- ✅ **Real-time Generation Progress**
- ✅ **Video Preview & Download**
- ✅ **Customizable Parameters**
- ✅ **Beautiful Modern UI**

### API Endpoints
- ✅ **POST /generate** - Generate video from image
- ✅ **GET /health** - Health check
- ✅ **GET /models** - List available models
- ✅ **GET /download/<filename>** - Download generated video
- ✅ **GET /jobs/<job_id>** - Get job status

## 📖 API Usage

### Generate Video from Image

```bash
curl -X POST http://localhost:5000/generate \
  -F "image=@your_image.jpg" \
  -F "prompt=A beautiful scene with gentle motion" \
  -F "video_length=17" \
  -F "resolution=720p" \
  -F "infer_steps=50"
```

### Response Example

```json
{
  "success": true,
  "video_url": "/download/abc123_generated.mp4",
  "job_id": "abc123",
  "parameters": {
    "prompt": "A beautiful scene with gentle motion",
    "video_length": 17,
    "infer_steps": 50,
    "resolution": "720p"
  },
  "processing_time": 2.0
}
```

## ⚙️ Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image` | File | Required | Image file (PNG, JPG, JPEG, WebP) |
| `prompt` | String | "A beautiful scene with motion" | Video description |
| `video_length` | Integer | 17 | Number of frames (17, 33, 65, 129) |
| `resolution` | String | "720p" | Video resolution (360p, 540p, 720p) |
| `infer_steps` | Integer | 50 | Quality steps (25, 50, 100) |
| `seed` | Integer | Random | Random seed for reproducibility |

## 🔧 Configuration

### File Limits
- **Max file size**: 10MB
- **Supported formats**: PNG, JPG, JPEG, WebP
- **Upload folder**: `/workspace/uploads`
- **Output folder**: `/workspace/results`

### Server Settings
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 5000
- **Debug mode**: Enabled
- **CORS**: Enabled

## 🌐 Network Access

### Local Access
- **URL**: http://localhost:5000
- **API**: http://localhost:5000/generate

### Remote Access (RunPod)
If running on RunPod, you can access it from anywhere:

1. **Get your RunPod IP**: Check the RunPod console
2. **Open port 5000**: RunPod should expose this automatically
3. **Access via**: http://YOUR_RUNPOD_IP:5000

### Example RunPod URL
```
http://213.173.105.4:5000
```

## 🛠️ Troubleshooting

### Common Issues

**1. "HunyuanVideo-I2V not available"**
```bash
# Check if HunyuanVideo-I2V is installed
conda activate hunyuan-i2v
cd /workspace/hunyuan-models/HunyuanVideo-I2V
python sample_image2video.py --help
```

**2. "Cannot connect to API server"**
```bash
# Check if server is running
ps aux | grep python
# Restart server
python start_server.py
```

**3. "Model loading failed"**
```bash
# Check GPU availability
nvidia-smi
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"
```

### Logs
Server logs are displayed in the terminal where you started the server. Check for:
- ✅ Model loading messages
- ❌ Error messages
- 🔄 Request processing logs

## 🔒 Security Notes

- **CORS enabled** for all origins (development only)
- **File uploads** are limited to 10MB
- **Generated files** are stored temporarily
- **No authentication** (add for production use)

## 📱 Mobile Support

The web interface is fully responsive and works on:
- ✅ **Desktop browsers**
- ✅ **Tablets**
- ✅ **Mobile phones**

## 🚀 Production Deployment

For production use, consider:

1. **Add authentication** (API keys, JWT tokens)
2. **Use a production WSGI server** (Gunicorn, uWSGI)
3. **Set up reverse proxy** (Nginx)
4. **Enable HTTPS** with SSL certificates
5. **Add rate limiting** to prevent abuse
6. **Implement proper logging** and monitoring

## 💡 Tips

- **Use shorter videos** (17 frames) for faster generation
- **Lower resolution** (360p) for quick previews
- **Higher infer_steps** (100) for better quality
- **Set a seed** for reproducible results
- **Stop the server** when not in use to save GPU costs

## 🤝 Contributing

Feel free to improve the web API:
- Add more video parameters
- Implement batch processing
- Add video editing features
- Improve the UI/UX
- Add user accounts and history

---

**Happy video generation! 🎬✨**
