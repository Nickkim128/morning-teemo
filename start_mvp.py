#!/usr/bin/env python3
"""
Quick start script for Morning News AI Assistant MVP
This script helps you get up and running quickly with minimal setup.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_file_exists(filepath):
    """Check if a file exists"""
    return Path(filepath).exists()

def create_env_file():
    """Create .env file from template"""
    if not check_file_exists('.env') and check_file_exists('env.example'):
        print("📝 Creating .env file from template...")
        subprocess.run(['cp', 'env.example', '.env'])
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your API keys:")
        print("   - NEWS_API_KEY (get from https://newsapi.org/)")
        print("   - GUARDIAN_API_KEY (get from https://open-platform.theguardian.com/)")
        print("   - OPENAI_API_KEY (get from https://openai.com/api/)")
        return False
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting backend server...")
    try:
        # Change to backend directory and start server
        os.chdir('backend')
        process = subprocess.Popen([sys.executable, 'main.py'])
        os.chdir('..')
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Test if server is running
        import requests
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully")
                return process
            else:
                print("❌ Backend server not responding properly")
                return None
        except requests.exceptions.RequestException:
            print("❌ Backend server not reachable")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def test_api_keys():
    """Test if API keys are configured"""
    print("🔑 Testing API configuration...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    news_api_key = os.getenv('NEWS_API_KEY')
    guardian_api_key = os.getenv('GUARDIAN_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not news_api_key or news_api_key == 'your_news_api_key_here':
        print("⚠️  NEWS_API_KEY not configured")
        return False
    
    if not openai_api_key or openai_api_key == 'your_openai_api_key_here':
        print("⚠️  OPENAI_API_KEY not configured")
        return False
    
    print("✅ API keys configured")
    return True

def main():
    """Main setup and start function"""
    print("🌅 Morning News AI Assistant - Quick Start")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if we're in the right directory
    if not check_file_exists('requirements.txt'):
        print("❌ Please run this script from the project root directory")
        return
    
    # Create .env file if needed
    if not create_env_file():
        print("\n📝 Please edit your .env file with the required API keys, then run this script again.")
        return
    
    # Test API keys
    if not test_api_keys():
        print("\n📝 Please configure your API keys in the .env file, then run this script again.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    print("\n🎉 MVP Backend is running!")
    print("=" * 50)
    print("Backend API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("\n📋 What you can do now:")
    print("1. Test the API: python test_backend.py")
    print("2. Try the briefing: curl http://localhost:8000/api/news/briefing")
    print("3. Set up frontend: cd frontend && npm install && npm run dev")
    print("\n⚠️  Press Ctrl+C to stop the server")
    
    try:
        # Keep the server running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    main() 