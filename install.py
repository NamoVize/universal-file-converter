#!/usr/bin/env python3
"""
Installation script for the Universal File Converter
"""
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print("Error: Python 3.8 or higher is required")
        return False
    return True


def create_virtual_environment():
    """Create a virtual environment"""
    print("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to create virtual environment")
        return False


def install_requirements():
    """Install requirements from requirements.txt"""
    print("Installing requirements...")
    
    # Determine the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_executable = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_executable = os.path.join("venv", "bin", "python")
    
    # Ensure the executable exists
    if not os.path.exists(python_executable):
        print(f"Error: Virtual environment Python executable not found at {python_executable}")
        return False
    
    try:
        subprocess.check_call([python_executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install requirements")
        return False


def install_package():
    """Install the package in development mode"""
    print("Installing the package...")
    
    # Determine the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_executable = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_executable = os.path.join("venv", "bin", "python")
    
    try:
        subprocess.check_call([python_executable, "-m", "pip", "install", "-e", "."])
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install the package")
        return False


def check_external_dependencies():
    """Check if external dependencies are installed"""
    print("Checking external dependencies...")
    
    missing_deps = []
    
    # Check for FFmpeg (for video conversions)
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            missing_deps.append("FFmpeg")
    except FileNotFoundError:
        missing_deps.append("FFmpeg")
    
    # Check for LibreOffice (for document conversions)
    try:
        if platform.system() == "Windows":
            cmd = ["soffice", "--version"]
        else:
            cmd = ["libreoffice", "--version"]
            
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            missing_deps.append("LibreOffice")
    except FileNotFoundError:
        missing_deps.append("LibreOffice")
    
    if missing_deps:
        print("Warning: The following external dependencies are missing:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nSome conversion features may not work without these dependencies.")
        print("Please install them manually according to your operating system.")
    else:
        print("All external dependencies are installed.")


def create_screenshots_dir():
    """Create screenshots directory if it doesn't exist"""
    screenshots_dir = Path("screenshots")
    if not screenshots_dir.exists():
        screenshots_dir.mkdir()
        print("Created screenshots directory")


def main():
    """Main installation function"""
    print("=" * 60)
    print("Universal File Converter - Installation")
    print("=" * 60)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Install the package
    if not install_package():
        return False
    
    # Check external dependencies
    check_external_dependencies()
    
    # Create screenshots directory
    create_screenshots_dir()
    
    print("\nInstallation completed successfully!")
    print("\nTo run the application:")
    
    if platform.system() == "Windows":
        print("  venv\\Scripts\\python src\\main.py")
    else:
        print("  source venv/bin/activate")
        print("  python src/main.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)