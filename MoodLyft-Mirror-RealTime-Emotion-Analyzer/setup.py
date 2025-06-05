#!/usr/bin/env python3
"""
Setup script for MoodLyft-Mirror
Automates installation and initial configuration
"""

import os
import sys
import subprocess
import platform
import json
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

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible!")
    return True

def check_system_requirements():
    """Check system requirements and recommend settings"""
    print("🖥️  Analyzing system capabilities...")
    
    system_info = {
        "os": platform.system(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor() or "Unknown",
    }
    
    try:
        import psutil
        system_info.update({
            "cpu_cores": psutil.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 1),
            "cpu_percent": psutil.cpu_percent(interval=1)
        })
    except ImportError:
        print("📦 Installing psutil for system analysis...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], 
                          check=True, capture_output=True)
            import psutil
            system_info.update({
                "cpu_cores": psutil.cpu_count(),
                "memory_gb": round(psutil.virtual_memory().total / (1024**3), 1),
                "cpu_percent": psutil.cpu_percent(interval=1)
            })
        except (subprocess.CalledProcessError, ImportError):
            print("   ⚠️  Could not install psutil, using basic detection")
            system_info.update({
                "cpu_cores": "Unknown",
                "memory_gb": "Unknown",
                "cpu_percent": "Unknown"
            })
    
    print(f"   OS: {system_info['os']} ({system_info['architecture']})")
    print(f"   CPU: {system_info.get('cpu_cores', 'Unknown')} cores")
    print(f"   Memory: {system_info.get('memory_gb', 'Unknown')} GB")
    
    # Recommend performance preset
    if isinstance(system_info.get('cpu_cores'), int) and isinstance(system_info.get('memory_gb'), (int, float)):
        if system_info['cpu_cores'] >= 8 and system_info['memory_gb'] >= 16:
            recommended_preset = "high_performance"
            print("🚀 Recommended preset: High Performance")
        elif system_info['cpu_cores'] >= 4 and system_info['memory_gb'] >= 8:
            recommended_preset = "balanced"
            print("⚖️  Recommended preset: Balanced")
        else:
            recommended_preset = "performance_mode"
            print("🔋 Recommended preset: Performance Mode")
    else:
        recommended_preset = "balanced"
        print("⚖️  Recommended preset: Balanced (default)")
    
    return system_info, recommended_preset

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine which requirements file to use
    system = platform.system().lower()
    
    if system == "darwin" and os.path.exists("requirements-macos.txt"):
        requirements_file = "requirements-macos.txt"
    elif system == "windows" and os.path.exists("requirements-windows.txt"):
        requirements_file = "requirements-windows.txt"
    else:
        # Create a basic requirements file
        basic_requirements = [
            "opencv-python>=4.8.0",
            "numpy>=1.24.0",
            "fer>=22.5.1",
            "pyttsx3>=2.90",
            "Pillow>=10.0.0",
            "scipy>=1.10.0",
            "matplotlib>=3.7.0",
            "psutil>=5.9.0"
        ]
        
        with open("requirements-basic.txt", "w") as f:
            f.write("\n".join(basic_requirements))
        
        requirements_file = "requirements-basic.txt"
    
    print(f"   Using {requirements_file}")
    
    try:
        # Try to upgrade pip first (optional, don't fail if this doesn't work)
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          check=True, capture_output=True)
            print("   ✅ pip upgraded successfully")
        except subprocess.CalledProcessError:
            print("   ⚠️  pip upgrade skipped (not critical)")
        
        # Install requirements
        print("   📦 Installing packages...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], 
                              check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"   Error details: {e.stderr}")
        elif hasattr(e, 'output') and e.output:
            print(f"   Output: {e.output}")
        
        print("\n🔧 Troubleshooting suggestions:")
        print("   1. Try running: pip install -r requirements-macos.txt")
        print("   2. Check if you have write permissions")
        print("   3. Try using a virtual environment:")
        print("      python3 -m venv venv")
        print("      source venv/bin/activate")
        print("      pip install -r requirements-macos.txt")
        
        return False

def create_config_file(recommended_preset):
    """Create a user configuration file"""
    print("⚙️  Creating configuration file...")
    
    config_content = f'''"""
User configuration for MoodLyft-Mirror
Generated by setup script
"""

from config import HardwarePresets, PerformanceConfig, VisualConfig, AudioConfig

# Apply recommended preset based on your hardware
HardwarePresets.{recommended_preset}()

# Customize these settings as needed:

# Performance (adjust based on your system)
# PerformanceConfig.EMOTION_SKIP_FRAMES = 3
# PerformanceConfig.CAMERA_WIDTH = 1280
# PerformanceConfig.CAMERA_HEIGHT = 720

# Visual effects (disable if experiencing performance issues)
# VisualConfig.ENABLE_ANIMATIONS = True
# VisualConfig.ENABLE_GLASSMORPHISM = True
# VisualConfig.ENABLE_GLOW_EFFECTS = True

# Audio settings
# AudioConfig.TTS_RATE = 160
# AudioConfig.COMPLIMENT_COOLDOWN = 8

print(f"🎯 Applied {recommended_preset.replace('_', ' ').title()} preset")
'''
    
    try:
        with open("user_config.py", "w") as f:
            f.write(config_content)
        print("✅ Configuration file created: user_config.py")
        return True
    except Exception as e:
        print(f"⚠️  Could not create config file: {e}")
        return False

def test_camera():
    """Test camera access"""
    print("📷 Testing camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Could not access camera (index 0)")
            # Try other camera indices
            for i in range(1, 4):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    print(f"✅ Camera found at index {i}")
                    cap.release()
                    return True
                cap.release()
            
            print("❌ No cameras found. Please ensure:")
            print("   - Camera is connected and not in use by other apps")
            print("   - Camera permissions are granted")
            return False
        else:
            print("✅ Camera access successful!")
            cap.release()
            return True
            
    except ImportError:
        print("⚠️  OpenCV not available for camera test")
        return True  # Assume it will work
    except Exception as e:
        print(f"⚠️  Camera test error: {e}")
        return True  # Don't fail setup for this

def create_project_launcher():
    """Create launcher script in project folder"""
    print("🖥️  Creating project launcher...")
    
    system = platform.system().lower()
    current_dir = os.getcwd()
    
    try:
        if system == "windows":
            # Windows batch file
            shortcut_path = "run_moodlyft.bat"
            
            with open(shortcut_path, "w") as f:
                f.write(f"""@echo off
echo 🚀 Starting MoodLyft-Mirror...
echo    Press Ctrl+C to quit
cd /d "{current_dir}"
python main.py
pause
""")
            print(f"✅ Launcher created: {shortcut_path}")
            
        elif system == "darwin":
            # macOS command file
            shortcut_path = "run_moodlyft.command"
            
            with open(shortcut_path, "w") as f:
                f.write(f"""#!/bin/bash
echo "🚀 Starting MoodLyft-Mirror..."
echo "   Press 'q' to quit, 's' for screenshot, 'r' to reset history"
cd "{current_dir}"

# Activate virtual environment if it exists
if [ -d "moodlyft_env" ]; then
    source moodlyft_env/bin/activate
fi

python3 main.py

# Keep terminal open briefly
echo ""
echo "✨ MoodLyft-Mirror closed. Press any key to exit..."
read -n 1 -s
""")
            
            os.chmod(shortcut_path, 0o755)
            print(f"✅ Launcher created: {shortcut_path}")
            
        else:
            # Linux shell script
            shortcut_path = "run_moodlyft.sh"
            
            with open(shortcut_path, "w") as f:
                f.write(f"""#!/bin/bash
echo "🚀 Starting MoodLyft-Mirror..."
echo "   Press 'q' to quit, 's' for screenshot, 'r' to reset history"
cd "{current_dir}"

# Activate virtual environment if it exists
if [ -d "moodlyft_env" ]; then
    source moodlyft_env/bin/activate
fi

python3 main.py

echo ""
echo "✨ MoodLyft-Mirror closed. Press any key to exit..."
read -n 1 -s
""")
            
            os.chmod(shortcut_path, 0o755)
            print(f"✅ Launcher created: {shortcut_path}")
            
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create launcher: {e}")
        return False

def run_demo():
    """Ask user if they want to run a demo"""
    print("\n🎉 Setup complete!")
    print("\nWould you like to:")
    print("1. 🚀 Run the application now")
    print("2. 🎭 Try the interactive demo")
    print("3. 📖 View the documentation")
    print("4. 🚪 Exit setup")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting MoodLyft-Mirror...")
        print("   Press 'q' to quit, 's' for screenshot, 'r' to reset history")
        try:
            subprocess.run([sys.executable, "main.py"])
        except KeyboardInterrupt:
            print("\n👋 Application closed by user")
        except Exception as e:
            print(f"\n❌ Error running application: {e}")
    
    elif choice == "2":
        print("\n🎭 Starting Interactive Demo...")
        print("   Press SPACE for next demo, 'q' to quit")
        try:
            subprocess.run([sys.executable, "demo.py"])
        except KeyboardInterrupt:
            print("\n👋 Demo closed by user")
        except Exception as e:
            print(f"\n❌ Error running demo: {e}")
    
    elif choice == "3":
        # Look for documentation files in current and parent directories
        readme_files = [
            "README.md",           # Current directory
            "../README.md",        # Parent directory
            "docs/README.md",      # Docs folder
            "../docs/README.md"    # Parent docs folder
        ]
        
        found_readme = False
        for readme in readme_files:
            if os.path.exists(readme):
                print(f"\n📖 Opening {readme}...")
                try:
                    if platform.system() == "Darwin":
                        subprocess.run(["open", readme])
                    elif platform.system() == "Windows":
                        subprocess.run(["start", readme], shell=True)
                    else:
                        subprocess.run(["xdg-open", readme])
                    found_readme = True
                    break
                except Exception as e:
                    print(f"   Could not open {readme}: {e}")
                    print(f"   Please manually open: {os.path.abspath(readme)}")
                    found_readme = True
                    break
        
        if not found_readme:
            print("   📖 Available documentation:")
            print("   - Check the project repository for README.md")
            print("   - Look for setup instructions in the parent directory")
            print("   - Visit the project homepage for online documentation")
    
    print("\n✨ Thank you for using MoodLyft-Mirror!")

def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        return
    
    # Analyze system
    system_info, recommended_preset = check_system_requirements()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        return
    
    # Create config
    create_config_file(recommended_preset)
    
    # Test camera
    test_camera()
    
    # Create launcher
    create_project_launcher()
    
    # Offer to run demo
    run_demo()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("Please check the documentation or report this issue") 