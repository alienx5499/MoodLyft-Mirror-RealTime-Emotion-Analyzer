#!/usr/bin/env python3
"""
Setup script for MoodLyft-Mirror
Automates virtual environment creation and dependency installation
Smart venv management - preserves existing working environments
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚀 MoodLyft-Mirror Setup                                  ║
║    Real-Time Emotion Analyzer with Modern UI                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def get_system_info():
    """Analyze system and return comprehensive information"""
    print("🖥️  Analyzing system capabilities...")
    
    system_info = {
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor() or "Unknown",
        "python_version": sys.version,
        "python_executable": sys.executable,
    }
    
    # Try to get additional system info
    try:
        import psutil
        system_info.update({
            "cpu_cores": psutil.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 1),
            "disk_free_gb": round(psutil.disk_usage('.').free / (1024**3), 1)
        })
    except ImportError:
        # psutil not available, use basic detection
        system_info.update({
            "cpu_cores": os.cpu_count() or "Unknown",
            "memory_gb": "Unknown",
            "disk_free_gb": "Unknown"
        })
    
    # Display system information
    print(f"   🖥️  OS: {system_info['os']} {system_info['os_version']} ({system_info['architecture']})")
    print(f"   🐍 Python: {system_info['python_version'].split()[0]}")
    print(f"   🖥️  CPU: {system_info.get('cpu_cores', 'Unknown')} cores")
    print(f"   💾 Memory: {system_info.get('memory_gb', 'Unknown')} GB")
    print(f"   💽 Disk Space: {system_info.get('disk_free_gb', 'Unknown')} GB free")
    
    return system_info

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        print("   Please install a newer Python version and try again.")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible!")
    return True

def get_venv_info():
    """Get virtual environment paths and commands for current system"""
    system = platform.system().lower()
    venv_name = "moodlyft_env"
    
    if system == "windows":
        venv_python = os.path.join(venv_name, "Scripts", "python.exe")
        venv_pip = os.path.join(venv_name, "Scripts", "pip.exe")
        activate_script = os.path.join(venv_name, "Scripts", "activate.bat")
    else:
        venv_python = os.path.join(venv_name, "bin", "python")
        venv_pip = os.path.join(venv_name, "bin", "pip")
        activate_script = os.path.join(venv_name, "bin", "activate")
    
    return {
        "name": venv_name,
        "python": venv_python,
        "pip": venv_pip,
        "activate": activate_script,
        "exists": os.path.exists(venv_name)
    }

def test_venv_health():
    """Test if existing virtual environment is healthy and working"""
    venv_info = get_venv_info()
    
    if not venv_info["exists"]:
        return False, "Virtual environment doesn't exist"
    
    # Check if Python executable exists
    if not os.path.exists(venv_info["python"]):
        return False, "Python executable missing in venv"
    
    # Test if Python works in the venv
    try:
        result = subprocess.run([
            venv_info["python"], "--version"
        ], check=True, capture_output=True, text=True)
        
        python_version = result.stdout.strip()
        print(f"   📍 Found existing venv with {python_version}")
        
    except subprocess.CalledProcessError:
        return False, "Python executable in venv is corrupted"
    
    # Test basic imports
    basic_modules = ["sys", "os", "subprocess"]
    for module in basic_modules:
        try:
            subprocess.run([
                venv_info["python"], "-c", f"import {module}"
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            return False, f"Basic module {module} import failed"
    
    return True, "Virtual environment is healthy"

def check_installed_packages():
    """Check what packages are already installed in the venv"""
    venv_info = get_venv_info()
    
    if not venv_info["exists"]:
        return {}
    
    try:
        result = subprocess.run([
            venv_info["pip"], "list", "--format=json"
        ], check=True, capture_output=True, text=True)
        
        import json
        packages = json.loads(result.stdout)
        return {pkg["name"].lower(): pkg["version"] for pkg in packages}
        
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}

def manage_virtual_environment():
    """Smart virtual environment management"""
    venv_info = get_venv_info()
    
    print("🔍 Checking virtual environment status...")
    
    if venv_info["exists"]:
        print("✅ Virtual environment found!")
        
        # Test if it's healthy
        is_healthy, health_message = test_venv_health()
        print(f"   Status: {health_message}")
        
        if is_healthy:
            print("🎯 Using existing virtual environment (no changes needed)")
            
            # Check if core packages are installed
            installed_packages = check_installed_packages()
            core_packages = ["opencv-python", "numpy", "pillow", "pyttsx3"]
            missing_packages = []
            
            for pkg in core_packages:
                if pkg.lower() not in installed_packages:
                    missing_packages.append(pkg)
            
            if missing_packages:
                print(f"   📦 Some packages missing: {', '.join(missing_packages)}")
                print("   Will update dependencies...")
                return True, "update"
            else:
                print("   📦 Core packages found")
                
                # Ask user if they want to update anyway
                choice = input("\n❓ Virtual environment looks good. Update dependencies anyway? (y/N): ").strip().lower()
                if choice in ['y', 'yes']:
                    return True, "update"
                else:
                    print("✅ Skipping dependency installation")
                    return True, "skip"
        else:
            print("⚠️  Virtual environment has issues - will recreate")
            
            # Ask for confirmation
            choice = input("\n❓ Recreate virtual environment? (Y/n): ").strip().lower()
            if choice in ['', 'y', 'yes']:
                return False, "recreate"
            else:
                print("❌ Cannot proceed with corrupted virtual environment")
                return False, "abort"
    else:
        print("📁 No virtual environment found - will create new one")
        return False, "create"

def remove_existing_venv():
    """Remove existing virtual environment if needed"""
    venv_info = get_venv_info()
    
    if venv_info["exists"]:
        print(f"🗑️  Removing existing virtual environment: {venv_info['name']}")
        try:
            # On Windows, sometimes files are locked, so try multiple approaches
            if platform.system().lower() == "windows":
                # Try to deactivate any active venv first
                try:
                    subprocess.run(["deactivate"], shell=True, capture_output=True)
                except:
                    pass
            
            shutil.rmtree(venv_info["name"])
            print("✅ Existing virtual environment removed successfully!")
            return True
            
        except PermissionError:
            print(f"❌ Permission denied. Please manually delete the '{venv_info['name']}' folder")
            print("   and run setup again.")
            return False
        except Exception as e:
            print(f"❌ Error removing virtual environment: {e}")
            print(f"   Please manually delete the '{venv_info['name']}' folder")
            return False
    
    return True

def create_virtual_environment():
    """Create a new virtual environment"""
    venv_info = get_venv_info()
    
    print(f"🏗️  Creating virtual environment: {venv_info['name']}")
    
    try:
        # Create virtual environment
        subprocess.run([
            sys.executable, "-m", "venv", venv_info["name"]
        ], check=True, capture_output=True)
        
        print("✅ Virtual environment created successfully!")
        
        # Verify creation
        if not os.path.exists(venv_info["python"]):
            print("❌ Virtual environment creation failed - Python executable not found")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {e}")
        print("   Make sure you have the 'venv' module available.")
        print("   Try running: python -m venv --help")
        return False
    except Exception as e:
        print(f"❌ Unexpected error creating virtual environment: {e}")
        return False

def upgrade_pip_in_venv():
    """Upgrade pip in the virtual environment"""
    venv_info = get_venv_info()
    
    print("📦 Upgrading pip in virtual environment...")
    
    try:
        subprocess.run([
            venv_info["python"], "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        
        print("✅ pip upgraded successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  pip upgrade failed: {e}")
        print("   Continuing with existing pip version...")
        return True  # Not critical, continue anyway

def install_requirements_in_venv():
    """Install requirements.txt in the virtual environment"""
    venv_info = get_venv_info()
    
    # Find the appropriate requirements file - prioritize platform-specific ones
    system = platform.system().lower()
    if system == "darwin":
        requirements_files = ["requirements-macos.txt", "requirements.txt"]
    elif system == "windows":
        requirements_files = ["requirements-windows.txt", "requirements.txt"]
    else:
        requirements_files = ["requirements.txt", "requirements-macos.txt", "requirements-windows.txt"]
    
    requirements_file = None
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            requirements_file = req_file
            break
    
    if not requirements_file:
        print("❌ No requirements file found!")
        print("   Looking for: requirements.txt, requirements-macos.txt, or requirements-windows.txt")
        return False
    
    print(f"📦 Installing/updating dependencies from {requirements_file}...")
    
    try:
        # Install requirements using virtual environment pip
        result = subprocess.run([
            venv_info["pip"], "install", "-r", requirements_file, "--upgrade"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed/updated successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"   Error details: {e.stderr}")
        
        print("\n🔧 Troubleshooting suggestions:")
        print(f"   1. Try manually: {venv_info['python']} -m pip install -r {requirements_file}")
        print("   2. Check if you have internet connectivity")
        print("   3. Some packages might require system dependencies")
        
        return False

def test_installation():
    """Test the installation by importing key modules"""
    venv_info = get_venv_info()
    
    print("🧪 Testing installation...")
    
    test_imports = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow"),
        ("pyttsx3", "pyttsx3")
    ]
    
    failed_imports = []
    
    for module, name in test_imports:
        try:
            result = subprocess.run([
                venv_info["python"], "-c", f"import {module}; print('{name} OK')"
            ], check=True, capture_output=True, text=True)
            print(f"   ✅ {name}")
        except subprocess.CalledProcessError:
            print(f"   ❌ {name}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  Some modules failed to import: {', '.join(failed_imports)}")
        print("   The application might not work correctly.")
        return False
    else:
        print("✅ All core modules imported successfully!")
        return True

def create_activation_scripts():
    """Create convenient activation scripts"""
    venv_info = get_venv_info()
    system = platform.system().lower()
    
    print("📝 Creating/updating activation scripts...")
    
    try:
        if system == "windows":
            # Windows batch file
            with open("activate_env.bat", "w") as f:
                f.write(f"""@echo off
echo 🐍 Activating MoodLyft virtual environment...
call {venv_info['activate']}
echo ✅ Virtual environment activated!
echo    You can now run: python main.py
cmd /k
""")
            print("✅ Created/updated activate_env.bat")
            
        else:
            # Unix shell script
            with open("activate_env.sh", "w") as f:
                f.write(f"""#!/bin/bash
echo "🐍 Activating MoodLyft virtual environment..."
source {venv_info['activate']}
echo "✅ Virtual environment activated!"
echo "   You can now run: python main.py"
bash
""")
            os.chmod("activate_env.sh", 0o755)
            print("✅ Created/updated activate_env.sh")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create activation scripts: {e}")
        return False

def create_run_script():
    """Create a script to run the application with the virtual environment"""
    venv_info = get_venv_info()
    system = platform.system().lower()
    
    print("🚀 Creating/updating run script...")
    
    try:
        if system == "windows":
            # Windows batch file
            with open("run_moodlyft.bat", "w") as f:
                f.write(f"""@echo off
echo 🚀 Starting MoodLyft-Mirror...
echo    Press 'q' to quit, 's' for screenshot, 'r' to reset history
echo    Press Ctrl+C to force quit
echo.

REM Change to script directory to ensure correct paths
cd /d "%~dp0"
echo 📁 Working directory: %CD%

REM Check if virtual environment exists
if not exist "{venv_info['name']}" (
    echo ❌ Virtual environment not found!
    echo    Expected location: %CD%\\{venv_info['name']}
    echo    Please run setup.py first
    pause
    exit /b 1
)

echo ✅ Virtual environment found: {venv_info['name']}

REM Activate virtual environment and run
call {venv_info['activate']}
{venv_info['python']} main.py

echo.
echo ✨ MoodLyft-Mirror closed. Press any key to exit...
pause
""")
            print("✅ Created/updated run_moodlyft.bat")
            
        else:
            # Unix shell script with smart path detection
            with open("run_moodlyft.sh", "w") as f:
                f.write(f"""#!/bin/bash

echo "🚀 Starting MoodLyft-Mirror..."
echo "   Press 'q' to quit, 's' for screenshot, 'r' to reset history"
echo "   Press Ctrl+C to force quit"
echo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" &> /dev/null && pwd )"
echo "📁 Script location: $SCRIPT_DIR"

# Change to script directory to ensure correct paths
cd "$SCRIPT_DIR"
echo "📁 Working directory: $(pwd)"

# Check if virtual environment exists in current directory
if [ ! -d "{venv_info['name']}" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Expected location: $(pwd)/{venv_info['name']}"
    echo "   Current files:"
    ls -la | head -10
    echo "   ..."
    echo
    echo "💡 Troubleshooting:"
    echo "   1. Make sure you're running this script from the correct directory"
    echo "   2. Run: python3 setup.py (to create virtual environment)"
    echo "   3. Check if {venv_info['name']} folder exists"
    exit 1
fi

echo "✅ Virtual environment found: {venv_info['name']}"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    echo "   Expected location: $(pwd)/main.py"
    echo "   Make sure you're in the correct MoodLyft directory"
    exit 1
fi

echo "✅ main.py found"

# Activate virtual environment and run
echo "🐍 Activating virtual environment..."
source {venv_info['activate']}

echo "🎬 Starting application..."
{venv_info['python']} main.py

echo ""
echo "✨ MoodLyft-Mirror closed. Press any key to exit..."
read -n 1 -s
""")
            os.chmod("run_moodlyft.sh", 0o755)
            print("✅ Created/updated run_moodlyft.sh")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create run script: {e}")
        return False

def display_usage_instructions():
    """Display usage instructions"""
    venv_info = get_venv_info()
    system = platform.system().lower()
    
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    
    print("\n📖 How to use:")
    
    if system == "windows":
        print("   Option 1 (Recommended): Double-click run_moodlyft.bat")
        print("   Option 2: Manual activation:")
        print("      1. Double-click activate_env.bat")
        print("      2. Run: python main.py")
    else:
        print("   Option 1 (Recommended): ./run_moodlyft.sh")
        print("   Option 2: Manual activation:")
        print("      1. source activate_env.sh")
        print("      2. python main.py")
    
    print("\n🎮 Controls:")
    print("   • Press 'q' to quit")
    print("   • Press 's' to take screenshot")
    print("   • Press 'r' to reset emotion history")
    
    print(f"\n📁 Virtual environment: {venv_info['name']}/")
    print(f"🐍 Python executable: {venv_info['python']}")
    
    print("\n💡 Tips:")
    print("   • Run setup.py again anytime to update dependencies")
    print("   • Ensure your camera is connected and not in use")
    print("   • Good lighting improves emotion detection")
    print("   • Position your face clearly in the camera view")

def main():
    """Main setup function"""
    # Step 0: Change to script directory to ensure relative paths work correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    original_dir = os.getcwd()
    os.chdir(script_dir)
    print(f"🔧 Working in script directory: {script_dir}")
    
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return 1
    
    # Step 2: Analyze system
    system_info = get_system_info()
    
    # Step 3: Smart virtual environment management
    venv_exists, action = manage_virtual_environment()
    
    if action == "abort":
        print("❌ Setup aborted by user")
        return 1
    elif action == "skip":
        print("⏭️  Skipping dependency installation")
    else:
        # Handle venv creation/recreation if needed
        if not venv_exists:
            if action == "recreate":
                if not remove_existing_venv():
                    return 1
            
            # Create new virtual environment
            if not create_virtual_environment():
                return 1
        
        # Step 4: Upgrade pip in virtual environment
        upgrade_pip_in_venv()
        
        # Step 5: Install/update requirements in virtual environment
        if action != "skip":
            if not install_requirements_in_venv():
                return 1
        
        # Step 6: Test installation
        if not test_installation():
            print("⚠️  Installation test failed, but continuing...")
    
    # Step 7: Create/update convenience scripts (always do this)
    create_activation_scripts()
    create_run_script()
    
    # Step 8: Display usage instructions
    display_usage_instructions()
    
    return 0

if __name__ == "__main__":
    original_dir = os.getcwd()
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        os.chdir(original_dir)  # Restore original directory
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("Please check the error above and try again.")
        os.chdir(original_dir)  # Restore original directory
        sys.exit(1) 