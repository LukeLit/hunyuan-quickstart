#!/usr/bin/env python3
"""
Simple, working web interface for HunyuanVideo-I2V
This creates an actual web server that works with RunPod
"""

import os
import sys
import subprocess
import tempfile
import shutil
from flask import Flask, request, jsonify, render_template_string, send_from_directory
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Create directories
UPLOAD_FOLDER = '/workspace/uploads'
RESULTS_FOLDER = '/workspace/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Job tracking
jobs = {}

# Simple HTML template
HTML_TEMPLATE = '''
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
        input, textarea, button, select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #0f3460;
            border-radius: 5px;
            background: #1a1a2e;
            color: white;
            box-sizing: border-box;
        }
        button {
            background: #e94560;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        button:hover { background: #c73a52; }
        button:disabled { background: #666; cursor: not-allowed; }
        .status {
            margin: 20px 0;
            padding: 15px;
            background: #0f3460;
            border-radius: 5px;
            text-align: center;
        }
        .progress {
            width: 100%;
            height: 20px;
            background: #333;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-bar {
            height: 100%;
            background: #e94560;
            width: 0%;
            transition: width 0.3s ease;
        }
        .result {
            margin-top: 20px;
            text-align: center;
            display: none;
        }
        .result video {
            max-width: 100%;
            border-radius: 5px;
            margin: 10px 0;
        }
        .error {
            color: #ff6b6b;
            background: #2d1b1b;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 HunyuanVideo-I2V Web Interface</h1>
        
        <form id="videoForm" enctype="multipart/form-data">
            <div class="upload-area" onclick="document.getElementById('imageFile').click()">
                <p>📁 Click to upload an image</p>
                <input type="file" id="imageFile" name="image" accept="image/*" style="display: none;" required>
                <p id="fileName"></p>
            </div>
            
            <textarea name="prompt" placeholder="Describe the video you want to generate..." rows="3" required>An idle animation</textarea>
            
            <input type="number" name="video_length" value="17" min="1" max="200" placeholder="Video length (frames)">
            <input type="number" name="infer_steps" value="50" min="10" max="100" placeholder="Inference steps">
            
            <select name="resolution">
                <option value="720p">720p (1280x720)</option>
                <option value="540p">540p (960x540)</option>
                <option value="360p">360p (640x360)</option>
            </select>
            
            <button type="submit" id="generateBtn">🚀 Generate Video</button>
        </form>
        
        <div class="status" id="status" style="display: none;">
            <div id="statusText">Processing...</div>
            <div class="progress">
                <div class="progress-bar" id="progressBar"></div>
            </div>
        </div>
        
        <div class="result" id="result">
            <h3>Generated Video:</h3>
            <video id="videoPlayer" controls></video>
            <br>
            <a id="downloadLink" href="#" download class="button">Download Video</a>
        </div>
    </div>

    <script>
        let currentJobId = null;
        
        document.getElementById('imageFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('fileName').textContent = 'Selected: ' + file.name;
            }
        });
        
        document.getElementById('videoForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const generateBtn = document.getElementById('generateBtn');
            const status = document.getElementById('status');
            const result = document.getElementById('result');
            
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            status.style.display = 'block';
            result.style.display = 'none';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    currentJobId = data.job_id;
                    document.getElementById('statusText').textContent = 'Video generation started...';
                    pollStatus();
                } else {
                    throw new Error(data.error || 'Failed to start generation');
                }
            } catch (error) {
                document.getElementById('statusText').textContent = 'Error: ' + error.message;
                generateBtn.disabled = false;
                generateBtn.textContent = '🚀 Generate Video';
            }
        });
        
        async function pollStatus() {
            if (!currentJobId) return;
            
            try {
                const response = await fetch('/status/' + currentJobId);
                const data = await response.json();
                
                if (response.ok) {
                    const status = data.status;
                    const progress = data.progress || 0;
                    
                    document.getElementById('statusText').textContent = data.message;
                    document.getElementById('progressBar').style.width = progress + '%';
                    
                    if (status === 'completed') {
                        document.getElementById('result').style.display = 'block';
                        document.getElementById('videoPlayer').src = '/download/' + data.video_file;
                        document.getElementById('downloadLink').href = '/download/' + data.video_file;
                        document.getElementById('generateBtn').disabled = false;
                        document.getElementById('generateBtn').textContent = '🚀 Generate Video';
                        currentJobId = null;
                    } else if (status === 'failed') {
                        document.getElementById('statusText').textContent = 'Error: ' + data.error;
                        document.getElementById('generateBtn').disabled = false;
                        document.getElementById('generateBtn').textContent = '🚀 Generate Video';
                        currentJobId = null;
                    } else {
                        setTimeout(pollStatus, 2000);
                    }
                }
            } catch (error) {
                document.getElementById('statusText').textContent = 'Error checking status: ' + error.message;
                document.getElementById('generateBtn').disabled = false;
                document.getElementById('generateBtn').textContent = '🚀 Generate Video';
                currentJobId = null;
            }
        }
    </script>
</body>
</html>
'''

def run_video_generation(job_id, image_path, prompt, video_length, infer_steps, resolution):
    """Run the actual video generation"""
    try:
        jobs[job_id]['status'] = 'running'
        jobs[job_id]['message'] = 'Starting video generation...'
        
        # Change to the model directory
        model_dir = '/workspace/hunyuan-models/HunyuanVideo-I2V'
        
        # Run the command
        cmd = [
            "bash", "-c",
            f"cd {model_dir} && eval \"$(conda shell.bash hook)\" && conda activate hunyuan-i2v && python sample_image2video.py --i2v-mode --i2v-image-path {image_path} --prompt '{prompt}' --video-length {video_length} --infer-steps {infer_steps} --i2v-resolution {resolution}"
        ]
        
        jobs[job_id]['message'] = 'Running HunyuanVideo-I2V model...'
        jobs[job_id]['progress'] = 25
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            # Look for output video
            output_files = [f for f in os.listdir(model_dir) if f.endswith('.mp4')]
            if output_files:
                latest_video = max(output_files, key=lambda f: os.path.getctime(os.path.join(model_dir, f)))
                
                # Copy to results folder
                result_path = os.path.join(RESULTS_FOLDER, f"video_{job_id}_{latest_video}")
                shutil.copy2(os.path.join(model_dir, latest_video), result_path)
                
                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['message'] = 'Video generated successfully!'
                jobs[job_id]['progress'] = 100
                jobs[job_id]['video_file'] = os.path.basename(result_path)
            else:
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['message'] = 'No output video found'
                jobs[job_id]['error'] = 'No video file was generated'
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = 'Generation failed'
            jobs[job_id]['error'] = result.stderr or 'Unknown error'
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = 'Generation failed'
        jobs[job_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save uploaded file
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Get parameters
    prompt = request.form.get('prompt', 'An idle animation')
    video_length = request.form.get('video_length', '17')
    infer_steps = request.form.get('infer_steps', '50')
    resolution = request.form.get('resolution', '720p')
    
    # Create job
    job_id = str(int(time.time()))
    jobs[job_id] = {
        'status': 'pending',
        'message': 'Starting...',
        'progress': 0,
        'created_at': datetime.now().isoformat()
    }
    
    # Start generation in background
    thread = threading.Thread(target=run_video_generation, args=(job_id, filepath, prompt, video_length, infer_steps, resolution))
    thread.start()
    
    return jsonify({'job_id': job_id, 'message': 'Generation started'})

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(RESULTS_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    print("🚀 Starting HunyuanVideo-I2V Web Server...")
    print("📱 Web Interface: http://localhost:5000")
    print("🔌 API Endpoint: http://localhost:5000/generate")
    print("📖 Status Check: http://localhost:5000/status/<job_id>")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
