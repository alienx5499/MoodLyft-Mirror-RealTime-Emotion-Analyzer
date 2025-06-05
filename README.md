<div align="center">

# 🌟 **MoodLyft Mirror RealTime Emotion Analyzer** 🌟  
### *Elevating your mood with intelligent emotion detection*

![Build Passing](https://img.shields.io/badge/build-passing-success?style=flat-square)
![Python](https://img.shields.io/badge/python-v3.11-blue?style=flat-square)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer-RealTime-Emotion-Analyzer/blob/main/CONTRIBUTING.md)
[![License: MIT](https://custom-icon-badges.herokuapp.com/github/license/alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer-RealTime-Emotion-Analyzer?logo=law&logoColor=white)](https://github.com/alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer-RealTime-Emotion-Analyzer/blob/main/LICENSE)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-brightgreen?style=flat-square)
![Views](https://hits.dwyl.com/alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer-RealTime-Emotion-Analyzer.svg)
![⭐ GitHub stars](https://img.shields.io/github/stars/Alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer?style=social)
![🍴 GitHub forks](https://img.shields.io/github/forks/Alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer?style=social)
![Commits](https://badgen.net/github/commits/Alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer)
![🐛 GitHub issues](https://img.shields.io/github/issues/Alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer)
![📂 GitHub pull requests](https://img.shields.io/github/issues-pr/Alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer)
![💾 GitHub code size](https://img.shields.io/github/languages/code-size/Alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer)

</div>

---

## **📱 What is MoodLyft Mirror RealTime Emotion Analyzer?**

The **MoodLyft Mirror** is an advanced emotion detection project that leverages AI to:
- Recognize emotions in real-time through facial analysis.
- Provide uplifting and personalized compliments based on detected emotions.
- Utilize a sleek and modern UI to enhance user experience.

> *"Enhance your day by visualizing and understanding your emotions!"*

---

## **📚 Table of Contents**
1. [✨ Features](#-features)
2. [🦾 Tech Stack](#-tech-stack)
3. [📸 Screenshots](#-screenshots)
4. [👨‍🔧 Setup Instructions](#-setup-instructions)
5. [🎯 Target Audience](#-target-audience)
6. [🤝 Contributing](#-contributing)
7. [📜 License](#-license)

---

## **✨ Features**  

### **Advanced Emotion Detection**
- Real-time emotion recognition using advanced AI algorithms with MTCNN face detection
- Displays dominant emotions like happiness, sadness, anger, surprise, fear, and disgust
- Confidence levels and emotion history tracking
- Intelligent frame skipping for optimal performance

### **Personalized Compliments**
- Intelligent compliments tailored to your mood with 5+ variations per emotion
- Advanced text-to-speech (TTS) with voice selection and non-blocking audio
- Smart cooldown system for natural interaction timing
- Emoji integration for enhanced visual feedback

### **Modern Glassmorphism UI**
- Sleek, translucent interface with modern glassmorphism effects
- Smooth animations including pulsing borders and color transitions
- Dynamic gradient backgrounds that respond to emotions
- Real-time performance metrics with color-coded FPS display
- Animated confidence bars and emotion history graphs

### **Performance Optimizations**
- Intelligent frame processing with configurable skip rates
- Threaded audio processing for smooth operation
- Auto-hardware detection with optimized presets
- Memory management with circular buffers
- Cross-platform font optimization

---

## **🦾 Tech Stack**

### 🌐 **Core Technologies**
- **Python**: Core programming language.
- **OpenCV**: For real-time video processing and face detection.
- **FER**: Facial Expression Recognition library for emotion analysis.
- **Pillow**: For enhanced text rendering and UI effects.

### **Additional Libraries**
- **Pyttsx3**: For advanced TTS functionality with voice selection
- **NumPy**: For numerical operations and efficient data processing
- **SciPy**: For advanced mathematical computations and optimizations
- **Matplotlib**: For real-time emotion history visualization
- **Psutil**: For system monitoring and auto-performance tuning

---

## **📸 Screenshots**
<div align="center">

<table>
<tr>
  <td><img src="https://via.placeholder.com/250" alt="Emotion Detection" width="250px"></td>
  <td><img src="https://via.placeholder.com/250" alt="Modern UI" width="250px"></td>
  <td><img src="https://via.placeholder.com/250" alt="Compliments in Action" width="250px"></td>
</tr>
<tr>
  <td><b>Emotion Detection</b></td>
  <td><b>Modern UI</b></td>
  <td><b>Compliments in Action</b></td>
</tr>
</table>

</div>

---

## **👨‍🔧 Setup Instructions**

### **Prerequisites**
- Python 3.11 or higher installed on your system.
- A webcam for real-time emotion detection.
- Install required Python packages listed in `requirements.txt`.

### **Steps to Run the Project**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer-RealTime-Emotion-Analyzer.git
   cd MoodLyft-Mirror-RealTime-Emotion-Analyzer
   ```

2. **Set Up a Virtual Environment**
    Setting up a virtual environment ensures that your project's dependencies are isolated from your global Python installation, preventing version conflicts and promoting a clean development environment.

   *For macOS/Linux*
   1. **Create a virtual environment:**
     ```bash
    python3 -m venv moodlyft_env
    ```

   2. **Activate the virtual environment:**
     ```bash
    source moodlyft_env/bin/activate
    ```
   *For Windows*
   1. **Create a virtual environment:**
     ```bash
    python3 -m venv moodlyft_env
    ```

   2. **Activate the virtual environment:**
     ```bash
    moodlyft_env\Scripts\activate 
    ```
3. **Install Dependencies**
   *For macOS/Linux*
     ```bash
    pip install -r requirements-macos.txt
    ```

   *For Windows*
     ```bash
    pip install -r requirements-windows.txt
    ```

4. **Run the Setup Script (Recommended)**
   ```bash
   python setup.py
   ```
   *This will automatically detect your system and apply optimal settings*

   **OR manually run the application:**
   ```bash
   python main.py
   ```

5. **Experience the App**
   - Ensure your webcam is connected and accessible
   - Use keyboard controls: 'q' to quit, 's' for screenshot, 'r' to reset history
   - Try the interactive demo: `python demo.py`

### **⚙️ Performance Configuration**

The application automatically detects your hardware and applies optimal settings. You can customize performance in `config.py`:

```python
# Performance presets available:
from config import HardwarePresets

HardwarePresets.high_performance()  # For powerful systems
HardwarePresets.balanced()          # Default balanced mode  
HardwarePresets.performance_mode()  # For older hardware
HardwarePresets.battery_saver()     # For laptops/mobile
```

### **🎮 Controls**

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `s` | Save screenshot |
| `r` | Reset emotion history |

### **🎯 Performance Improvements**

| Metric | Original | Optimized | Improvement |
|--------|----------|-----------|-------------|
| FPS | 15-20 | 25-30 | +40-50% |
| Memory Usage | ~300MB | ~200MB | -33% |
| CPU Usage | ~40% | ~25% | -37% |
| TTS Blocking | Yes | No | Non-blocking |

---

## **🎯 Target Audience**

1. **Individuals**: Track your mood and uplift your spirits daily.
2. **Therapists**: Utilize emotion detection as part of therapy sessions.
3. **Developers**: Enhance and expand the project with additional features.

---

## **🤝 Contributing**

We ❤️ open source! Contributions are welcome to make this project even better.  

1. Fork the repository.  
2. Create your feature branch.  
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes.  
   ```bash
   git commit -m "Add a new feature"
   ```
4. Push to the branch and open a pull request.

---

## **📜 License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 📬 **Feedback & Suggestions**
*We value your input! Share your thoughts through [GitHub Issues](https://github.com/alienx5499/MoodLyft-Mirror-RealTime-Emotion-Analyzer-RealTime-Emotion-Analyzer/issues).*

💡 *Let's work together to uplift emotions and create positivity!*

</div>
