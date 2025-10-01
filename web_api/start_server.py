#!/usr/bin/env python3
"""
HunyuanVideo-I2V Web API Server Launcher
Starts the Flask web server with proper configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask_cors',
        'opencv-python',
        'pillow',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies.")
            print("Please run: pip install -r requirements.txt")
            return False
    
    return True

def check_hunyuan_setup():
    """Check if HunyuanVideo-I2V is properly set up"""
    hunyuan_path = Path("/workspace/hunyuan-models/HunyuanVideo-I2V")
    
    if not hunyuan_path.exists():
        print("❌ HunyuanVideo-I2V not found at /workspace/hunyuan-models/HunyuanVideo-I2V")
        print("Please run the installer first: ./cloud_setup/setup_cloud.sh")
        return False
    
    # Check if conda environment exists
    try:
        result = subprocess.run([
            'conda', 'env', 'list'
        ], capture_output=True, text=True, check=True)
        
        if 'hunyuan-i2v' not in result.stdout:
            print("❌ HunyuanVideo-I2V conda environment not found")
            print("Please run the installer first: ./cloud_setup/setup_cloud.sh")
            return False
        
        print("✅ HunyuanVideo-I2V setup found")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Cannot check conda environments")
        return False

def start_server():
    """Start the Flask web server"""
    print("🚀 Starting HunyuanVideo-I2V Web API Server...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check Hunyuan setup
    if not check_hunyuan_setup():
        return False
    
    # Set environment variables
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    # Start the server
    print("\n🌐 Starting web server...")
    print("📱 Web Interface: http://localhost:5000")
    print("🔌 API Endpoint: http://localhost:5000")
    print("📖 Health Check: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    start_server()
