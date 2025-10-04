# WePlay - Spider-Man: Miles Morales Automation

An advanced automation system for Spider-Man: Miles Morales featuring AI-powered path-following, obstacle detection, and automated gameplay scenarios.

## 🕷️ Features

### 🛤️ Path-Following System
- **Real-time path detection** using OpenCV edge detection
- **Continuous walk mode** with Left-Alt + W controls
- **Adaptive steering** based on path deviation
- **Works on curves and hills** with dynamic correction

### 🤖 AI-Powered Automation
- **YOLOv8n object detection** for buildings and obstacles
- **Central Park auto-walk** with obstacle avoidance
- **Auto-swing system** with building detection
- **Person detection** with automated responses

### 🎮 Game Controls
- **Dynamic command processor** with auto-completion
- **Command history** with persistent storage
- **Multi-game support** with service registry
- **Keyboard input simulation** using pydirectinput

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r A/Game_Services/SpManMM_Service/Scenario_Scripts/requirements_yolo.txt
   ```

2. **Launch the Command Processor:**
   ```bash
   python command_processor.py
   ```

3. **Available Commands:**
   - `path follow` - Start path-following system
   - `auto walk` - Continuous walking with obstacle detection
   - `auto swing` - AI-powered building avoidance swinging
   - `super jump` - Enhanced momentum jump
   - `web swing combo` - Complex swinging sequence

## 📁 Project Structure

```
A/Game_Services/SpManMM_Service/
├── Basic_Movement/          # Basic movement controls
├── Camera_Controls/         # Camera manipulation
├── Special_Abilities/       # Special moves and abilities
├── Scenario_Scripts/        # Composite automation scripts
│   ├── yolo_building_detector.py  # AI detection system
│   ├── scenario_scripts.py        # Main automation logic
│   └── requirements_yolo.txt      # AI dependencies
└── SPIDERMAN_COMMAND_LIST.md      # Complete command reference
```

## 🔧 Technical Details

### Path Detection Algorithm
- **HSV color filtering** for dark path vs. bright snow detection
- **Canny edge detection** for precise boundary identification
- **Horizontal scanning** fallback for difficult conditions
- **Spider-Man body measurements** for accurate positioning

### AI Detection System
- **YOLOv8n model** for real-time object detection
- **30 FPS processing** with optimized performance
- **Multi-class detection** (buildings, people, obstacles)
- **Proximity-based navigation** with distance calculations

### Control System
- **Window focus management** with multiple fallback methods
- **Keyboard input simulation** using pydirectinput
- **Threading support** for concurrent operations
- **Error handling** with graceful recovery

## 🎯 Usage Examples

### Path Following
```
Game> path follow
🛤️ Starting path-following with continuous walk mode...
🚶 Holding Left-Alt (walk mode) + W (forward) continuously...
🛤️ Path correction: too_far_right - offset: 45.2px
   ↖️ Left steering for 0.3s
```

### Auto-Swing
```
Game> auto swing
🚀 Auto-swing system started!
💡 Press 'End' key to stop auto-swing
🎯 Executing right_swing - avoid_close_left (close proximity, 2 buildings)
```

## 🛠️ Requirements

- Python 3.8+
- Windows 10/11 (for game window management)
- Spider-Man: Miles Morales (PC version)
- YOLOv8 dependencies (see requirements_yolo.txt)

## 📝 License

This project is for educational and research purposes. Please respect the game's terms of service and use responsibly.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note:** This automation system is designed for educational purposes and showcases advanced computer vision and game automation techniques.
