#!/usr/bin/env python3
"""
Start the HunyuanVideo-I2V web server
This script handles all the setup and starts the Flask server
"""

import os
import sys
import subprocess

def print_status(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️ {message}")

def install_flask():
    """Install Flask if not available"""
    try:
        import flask
        print_status("Flask is already installed")
        return True
    except ImportError:
        print_warning("Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print_status("Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install Flask")
            return False

def check_model_setup():
    """Check if HunyuanVideo-I2V is set up"""
    model_dir = "/workspace/hunyuan-models/HunyuanVideo-I2V"
    if os.path.exists(model_dir):
        print_status("HunyuanVideo-I2V model found")
        return True
    else:
        print_warning("HunyuanVideo-I2V model not found")
        print_warning("Make sure you've run the installer first")
        return False

def start_server():
    """Start the web server"""
    print("🚀 Starting HunyuanVideo-I2V Web Server...")
    print("=" * 50)
    
    # Install Flask
    if not install_flask():
        return False
    
    # Check model setup
    check_model_setup()
    
    # Start the server
    print_status("Starting web server...")
    print("📱 Web Interface will be available at: http://localhost:5000")
    print("🔌 For RunPod access, use JupyterLab proxy: http://YOUR_IP:8888/proxy/5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from simple_working_interface import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print_error(f"Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_server()
