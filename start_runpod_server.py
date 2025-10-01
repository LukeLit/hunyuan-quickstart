#!/usr/bin/env python3
"""
Simple script to start the HunyuanVideo-I2V web API on RunPod
This script should be run on the RunPod instance, not locally
"""

import os
import sys
import subprocess
import time

def print_status(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️ {message}")

def check_runpod_environment():
    """Check if we're in a RunPod-like environment"""
    # Check for common RunPod indicators
    runpod_indicators = [
        "/workspace" in os.getcwd(),
        os.path.exists("/workspace"),
        os.environ.get("RUNPOD_POD_ID") is not None,
        "213.173.105.4" in os.environ.get("HOSTNAME", "")
    ]
    
    if any(runpod_indicators):
        print_status("RunPod environment detected")
        return True
    else:
        print_warning("This doesn't appear to be a RunPod environment")
        print_warning("Make sure you're running this on your RunPod instance")
        return False

def start_flask_server():
    """Start the Flask server"""
    try:
        # Change to the web API directory
        web_api_dir = "/workspace/hunyuan-quickstart/web_api"
        
        if not os.path.exists(web_api_dir):
            print_error(f"Web API directory not found: {web_api_dir}")
            print_error("Make sure you've run the installer and pulled the latest code")
            return False
        
        print_status(f"Changing to {web_api_dir}")
        os.chdir(web_api_dir)
        
        # Check if requirements are installed
        try:
            import flask
            import flask_cors
            print_status("Flask dependencies are available")
        except ImportError as e:
            print_warning(f"Missing dependencies: {e}")
            print_status("Installing requirements...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Start the server
        print_status("Starting Flask server on port 5000...")
        print_status("Access via JupyterLab proxy: http://YOUR_IP:8888/proxy/5000")
        
        # Import and run the Flask app
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        print_error(f"Failed to start Flask server: {e}")
        return False

if __name__ == "__main__":
    print("🚀 HunyuanVideo-I2V Web API Server Starter")
    print("=" * 50)
    
    if not check_runpod_environment():
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)
    
    print_status("Starting web API server...")
    start_flask_server()
