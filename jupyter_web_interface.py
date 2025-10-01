#!/usr/bin/env python3
"""
JupyterLab-compatible web interface for HunyuanVideo-I2V
This avoids the "Trust HTML" issues by using Jupyter widgets
"""

import os
import sys
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from IPython.display import Javascript
import base64
import io
from PIL import Image
import subprocess
import tempfile
import shutil

class HunyuanVideoInterface:
    def __init__(self):
        self.setup_interface()
        
    def setup_interface(self):
        """Create the web interface using Jupyter widgets"""
        
        # Create widgets
        self.file_upload = widgets.FileUpload(
            accept='image/*',
            multiple=False,
            description='Upload Image:'
        )
        
        self.prompt_text = widgets.Textarea(
            value='A beautiful sunset with gentle waves',
            placeholder='Describe the video you want to generate...',
            description='Prompt:',
            rows=3
        )
        
        self.video_length = widgets.IntSlider(
            value=17,
            min=1,
            max=200,
            description='Video Length:'
        )
        
        self.infer_steps = widgets.IntSlider(
            value=50,
            min=10,
            max=100,
            description='Inference Steps:'
        )
        
        self.resolution = widgets.Dropdown(
            options=['720p', '540p', '360p'],
            value='720p',
            description='Resolution:'
        )
        
        self.generate_button = widgets.Button(
            description='🚀 Generate Video',
            button_style='danger',
            layout=widgets.Layout(width='300px', height='40px')
        )
        
        self.status_output = widgets.Output()
        self.result_output = widgets.Output()
        
        # Connect the button
        self.generate_button.on_click(self.generate_video)
        
        # Display the interface
        self.display_interface()
        
    def display_interface(self):
        """Display the complete interface"""
        clear_output(wait=True)
        
        # Header
        display(HTML("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #e94560;">🎬 HunyuanVideo-I2V Interface</h1>
            <p style="color: #0f3460; font-size: 16px;">Generate videos from images using AI</p>
        </div>
        """))
        
        # Main interface
        display(widgets.VBox([
            widgets.HTML("<h3>📁 Upload an Image</h3>"),
            self.file_upload,
            widgets.HTML("<h3>✏️ Video Description</h3>"),
            self.prompt_text,
            widgets.HTML("<h3>⚙️ Settings</h3>"),
            self.video_length,
            self.infer_steps,
            self.resolution,
            widgets.HTML("<br>"),
            self.generate_button,
            widgets.HTML("<br>"),
            widgets.HTML("<h3>📊 Status</h3>"),
            self.status_output,
            widgets.HTML("<h3>🎥 Result</h3>"),
            self.result_output
        ]))
        
    def generate_video(self, button):
        """Handle video generation"""
        with self.status_output:
            clear_output(wait=True)
            
            # Check if image is uploaded
            if not self.file_upload.value:
                print("❌ Please upload an image first!")
                return
                
            print("🔄 Starting video generation...")
            print(f"📝 Prompt: {self.prompt_text.value}")
            print(f"⏱️ Length: {self.video_length.value} frames")
            print(f"🔧 Steps: {self.infer_steps.value}")
            print(f"📐 Resolution: {self.resolution.value}")
            
            # Save uploaded image
            if isinstance(self.file_upload.value, tuple):
                # Handle tuple format
                uploaded_file = self.file_upload.value[0]
            else:
                # Handle dict format
                uploaded_file = list(self.file_upload.value.values())[0]
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = os.path.join(temp_dir, "input_image.jpg")
                
                # Save the uploaded image
                with open(image_path, 'wb') as f:
                    f.write(uploaded_file['content'])
                
                print(f"💾 Image saved to: {image_path}")
                
                # Check if HunyuanVideo-I2V is available
                hunyuan_dir = "/workspace/hunyuan-models/HunyuanVideo-I2V"
                if not os.path.exists(hunyuan_dir):
                    print("❌ HunyuanVideo-I2V not found. Please run the installer first!")
                    return
                
                # Try to run the actual model
                try:
                    print("🚀 Running HunyuanVideo-I2V model...")
                    
                    # Change to the model directory
                    os.chdir(hunyuan_dir)
                    
                    # Activate conda environment and run the model
                    cmd = [
                        "bash", "-c",
                        f"eval \"$(conda shell.bash hook)\" && conda activate hunyuan-i2v && python sample_image2video.py --i2v-mode --i2v-image-path {image_path} --prompt '{self.prompt_text.value}' --video-length {self.video_length.value} --infer-steps {self.infer_steps.value} --i2v-resolution {self.resolution.value} --cfg-scale 1.0"
                    ]
                    
                    print("⚡ Executing command...")
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        print("✅ Video generation completed!")
                        
                        # Look for output video
                        output_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
                        if output_files:
                            latest_video = max(output_files, key=os.path.getctime)
                            print(f"🎥 Generated video: {latest_video}")
                            
                            # Copy to workspace for download
                            workspace_video = f"/workspace/{latest_video}"
                            shutil.copy2(latest_video, workspace_video)
                            
                            with self.result_output:
                                clear_output(wait=True)
                                display(HTML(f"""
                                <div style="text-align: center;">
                                    <h3>🎉 Video Generated Successfully!</h3>
                                    <p><strong>File:</strong> {latest_video}</p>
                                    <p><strong>Location:</strong> {workspace_video}</p>
                                    <p>You can download the video from your workspace.</p>
                                </div>
                                """))
                        else:
                            print("⚠️ No output video found")
                            
                    else:
                        print(f"❌ Error: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    print("⏰ Generation timed out (5 minutes)")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
                finally:
                    # Return to original directory
                    os.chdir("/workspace")

# Create and display the interface
interface = HunyuanVideoInterface()
