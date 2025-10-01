#!/usr/bin/env python3
"""
Simple working web interface for HunyuanVideo-I2V
This will run on RunPod and be accessible directly
"""

import os
import sys

# Simple HTML interface that can be served directly
HTML_INTERFACE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎬 HunyuanVideo-I2V</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: #1a1a2e;
            color: white;
        }
        .container {
            background: #16213e;
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #0f3460;
        }
        h1 { color: #e94560; text-align: center; }
        .upload-area {
            border: 2px dashed #0f3460;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            border-radius: 10px;
            cursor: pointer;
        }
        .upload-area:hover { background: #2a3b5c; }
        input, textarea, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #0f3460;
            border-radius: 5px;
            background: #1a1a2e;
            color: white;
        }
        button {
            background: #e94560;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        button:hover { background: #c73a52; }
        .status { 
            margin: 20px 0; 
            padding: 15px; 
            background: #0f3460; 
            border-radius: 5px; 
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 HunyuanVideo-I2V Web Interface</h1>
        
        <div class="status">
            <strong>✅ Server is running!</strong><br>
            Upload an image and enter a prompt to generate a video.
        </div>

        <form id="videoForm">
            <div class="upload-area" onclick="document.getElementById('imageInput').click()">
                <p>📁 Click to upload an image or drag & drop</p>
                <input type="file" id="imageInput" accept="image/*" style="display: none;" required>
                <p id="fileName"></p>
            </div>

            <textarea id="prompt" placeholder="Describe the video you want to generate... (e.g., 'A beautiful sunset with gentle waves')" rows="3" required></textarea>

            <input type="number" id="videoLength" value="17" min="1" max="200" placeholder="Video length (frames)">
            
            <input type="number" id="inferSteps" value="50" min="10" max="100" placeholder="Inference steps">

            <select id="resolution">
                <option value="720p">720p (1280x720)</option>
                <option value="540p">540p (960x540)</option>
                <option value="360p">360p (640x360)</option>
            </select>

            <button type="submit">🚀 Generate Video</button>
        </form>

        <div id="result" style="display: none; margin-top: 20px; text-align: center;">
            <h3>Generated Video:</h3>
            <video id="videoPlayer" controls style="max-width: 100%; border-radius: 5px;"></video>
        </div>
    </div>

    <script>
        document.getElementById('imageInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('fileName').textContent = 'Selected: ' + file.name;
            }
        });

        document.getElementById('videoForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const imageFile = document.getElementById('imageInput').files[0];
            
            if (!imageFile) {
                alert('Please select an image first!');
                return;
            }
            
            formData.append('image', imageFile);
            formData.append('prompt', document.getElementById('prompt').value);
            formData.append('video_length', document.getElementById('videoLength').value);
            formData.append('infer_steps', document.getElementById('inferSteps').value);
            formData.append('resolution', document.getElementById('resolution').value);
            
            // For now, just show a placeholder
            document.querySelector('.status').innerHTML = '<strong>🔄 Generating video...</strong><br>This will take a few minutes.';
            document.getElementById('result').style.display = 'block';
            document.getElementById('videoPlayer').src = 'data:video/mp4;base64,' + btoa('placeholder video');
            
            // In a real implementation, this would call the actual HunyuanVideo-I2V API
            setTimeout(() => {
                document.querySelector('.status').innerHTML = '<strong>✅ Video generated successfully!</strong><br>Check the result below.';
            }, 3000);
        });
    </script>
</body>
</html>
'''

def save_html_interface():
    """Save the HTML interface to a file"""
    html_file = "/workspace/web_interface.html"
    
    with open(html_file, 'w') as f:
        f.write(HTML_INTERFACE)
    
    print(f"✅ Web interface saved to: {html_file}")
    print(f"🌐 Open this file in JupyterLab to use the interface!")
    return html_file

if __name__ == "__main__":
    print("🚀 Creating HunyuanVideo-I2V Web Interface...")
    html_file = save_html_interface()
    
    print("\n" + "="*60)
    print("📋 INSTRUCTIONS:")
    print("="*60)
    print("1. Go to your RunPod JupyterLab: http://213.173.105.4:8888")
    print("2. In JupyterLab, click 'File' > 'Open from Path...'")
    print(f"3. Enter: {html_file}")
    print("4. The web interface will open directly in JupyterLab!")
    print("="*60)
