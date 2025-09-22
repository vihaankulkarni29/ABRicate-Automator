#!/usr/bin/env python3
"""
ABRicate Automater Setup Script
Automatically installs and configures ABRicate for seamless AMR analysis
"""

import os
import sys
import subprocess
import platform
import urllib.request
import shutil

def run_command(cmd, description=""):
    """Run a command and return success status"""
    print(f"[SETUP] {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e.stderr}")
        return False

def check_conda():
    """Check if conda is available"""
    try:
        result = subprocess.run(['conda', '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def install_miniconda():
    """Install Miniconda if not available"""
    print("Installing Miniconda...")

    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        installer_path = "miniconda_installer.exe"
        install_cmd = f'start /wait "" {installer_path} /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\\miniconda3'
    else:
        installer_url = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-{system}-{machine}.sh"
        installer_path = "miniconda_installer.sh"
        install_cmd = f"bash {installer_path} -b -p $HOME/miniconda3"

    # Download installer
    print(f"Downloading Miniconda installer...")
    urllib.request.urlretrieve(installer_url, installer_path)

    # Run installer
    if not run_command(install_cmd, "Installing Miniconda"):
        print("Miniconda installation failed")
        return False

    # Clean up
    os.remove(installer_path)

    # Add to PATH for current session
    if system == "windows":
        conda_path = os.path.expanduser("~/miniconda3/Scripts")
    else:
        conda_path = os.path.expanduser("~/miniconda3/bin")

    os.environ["PATH"] = conda_path + os.pathsep + os.environ.get("PATH", "")

    print("Miniconda installed successfully")
    return True

def setup_abricate_env():
    """Create and setup ABRicate conda environment"""
    print("Setting up ABRicate environment...")

    commands = [
        "conda config --add channels defaults",
        "conda config --add channels bioconda",
        "conda config --add channels conda-forge",
        "conda create -n abricate-env abricate -y",
        "conda activate abricate-env && abricate --setupdb"
    ]

    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            return False

    print("ABRicate environment ready")
    return True

def main():
    """Main setup function"""
    print("ABRicate Automater Setup")
    print("=" * 40)

    # Check if already setup
    try:
        result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
        if 'abricate-env' in result.stdout:
            print("ABRicate environment already exists")
            print("Run: conda activate abricate-env")
            print("Then: python abricate_automater.py --input-dir your/genomes --output-dir results")
            return
    except:
        pass

    # Install conda if needed
    if not check_conda():
        if not install_miniconda():
            print("Setup failed at Miniconda installation")
            sys.exit(1)

    # Setup ABRicate environment
    if not setup_abricate_env():
        print("Setup failed at ABRicate environment creation")
        sys.exit(1)

    print("\nSetup Complete!")
    print("\nTo use the ABRicate Automater:")
    print("1. conda activate abricate-env")
    print("2. python abricate_automater.py --input-dir your/genomes --output-dir results")
    print("\nYour AMR analysis pipeline is ready!")

if __name__ == "__main__":
    main()