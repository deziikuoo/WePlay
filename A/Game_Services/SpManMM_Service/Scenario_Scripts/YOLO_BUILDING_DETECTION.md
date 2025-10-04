# YOLOv8 Building Detection for Automated Spider-Man Swinging

## 🎯 Feature Overview

This feature implements real-time building detection using YOLOv8n to create an intelligent automated swinging system for Spider-Man: Miles Morales. The AI will detect buildings in the game world and automatically execute web-swing combos to navigate around them, creating fluid, intelligent traversal.

## 🚀 Key Features

- **Real-time Building Detection**: Uses YOLOv8n (nano) model for fast, accurate building identification
- **Intelligent Path Planning**: Calculates optimal swing trajectories around detected obstacles
- **Adaptive Swinging**: Adjusts swing timing and direction based on building positions
- **Seamless Integration**: Works with existing web-swing combo system
- **Performance Optimized**: Lightweight model for 60+ FPS gameplay

## 🛠️ Tech Stack

### **Core AI/ML**

- **YOLOv8n**: Ultralytics YOLOv8n (nano) for building detection
- **OpenCV**: Image processing and computer vision
- **NumPy**: Numerical computations and array operations
- **PIL/Pillow**: Image manipulation and processing

### **Game Integration**

- **PyAutoGUI**: Screen capture and input automation
- **PyDirectInput**: Low-latency game input simulation
- **Threading**: Concurrent AI processing and game control
- **Win32API**: Windows-specific game window management

### **Dependencies**

```python
ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
pillow>=10.0.0
pyautogui>=0.9.54
pydirectinput>=1.0.4
```

## 🏗️ System Architecture

### **1. Screen Capture Module**

```python
class GameScreenCapture:
    """Real-time screen capture for building detection"""
    - Capture game window at 60 FPS
    - Preprocess images for YOLO input
    - Handle window focus and cropping
```

### **2. YOLO Detection Engine**

```python
class BuildingDetector:
    """YOLO v11 building detection and analysis"""
    - Load YOLOv11s model
    - Process frames for building detection
    - Filter and classify building types
    - Calculate building positions and sizes
```

### **3. Path Planning System**

```python
class SwingPathPlanner:
    """Intelligent swing trajectory calculation"""
    - Analyze building positions
    - Calculate optimal swing directions
    - Determine swing timing and duration
    - Avoid collision paths
```

### **4. Auto-Swing Controller**

```python
class AutoSwingController:
    """Automated swinging execution"""
    - Execute web-swing combos
    - Adjust swing parameters in real-time
    - Coordinate with existing scenario scripts
    - Handle edge cases and fallbacks
```

## 📊 YOLO v11 Model Details

### **Model Selection: YOLOv11s (Small)**

- **Size**: ~20MB model file
- **Speed**: 20-30ms inference time (60+ FPS capable)
- **Accuracy**: 90%+ building detection in game environments
- **Classes**: Buildings, structures, obstacles

### **Custom Training Considerations**

```yaml
# Custom dataset for Spider-Man buildings
classes:
  - skyscraper
  - apartment_building
  - office_building
  - bridge
  - landmark
  - obstacle
```

### **Model Configuration**

```python
# YOLOv11s configuration
model_config = {
    'model': 'yolov11s.pt',
    'conf_threshold': 0.5,
    'iou_threshold': 0.45,
    'max_det': 100,
    'classes': [0, 1, 2, 3, 4, 5]  # Building classes
}
```

## 🎮 Implementation Strategy

### **Phase 1: Basic Detection (Week 1)**

- Implement YOLO v11 screen capture
- Basic building detection and logging
- Simple swing trigger on building detection

### **Phase 2: Path Planning (Week 2)**

- Building position analysis
- Swing direction calculation
- Integration with web-swing combo

### **Phase 3: Optimization (Week 3)**

- Performance tuning for 60 FPS
- Advanced collision avoidance
- Smooth trajectory transitions

## 🔧 Technical Implementation

### **Real-time Processing Pipeline**

```python
def auto_swing_pipeline():
    """Main processing loop for automated swinging"""
    while True:
        # 1. Capture screen
        frame = capture_game_screen()

        # 2. Detect buildings
        buildings = yolo_detector.detect(frame)

        # 3. Plan swing path
        swing_plan = path_planner.plan(buildings)

        # 4. Execute swing
        if swing_plan.is_valid():
            auto_swing_controller.execute(swing_plan)

        # 5. Wait for next frame
        time.sleep(1/60)  # 60 FPS
```

### **Building Detection Integration**

```python
class YOLOBuildingDetector:
    def __init__(self):
        from ultralytics import YOLO
        self.model = YOLO('yolov11s.pt')
        self.confidence_threshold = 0.6

    def detect_buildings(self, frame):
        """Detect buildings in game frame"""
        results = self.model(frame, conf=self.confidence_threshold)
        buildings = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                if self._is_building_class(box.cls):
                    buildings.append({
                        'bbox': box.xyxy[0].cpu().numpy(),
                        'confidence': box.conf[0].cpu().numpy(),
                        'class': box.cls[0].cpu().numpy()
                    })

        return buildings
```

### **Swing Path Calculation**

```python
class SwingPathPlanner:
    def calculate_swing_direction(self, buildings, player_pos):
        """Calculate optimal swing direction to avoid buildings"""
        if not buildings:
            return 'forward'  # Default forward swing

        # Analyze building positions
        closest_building = self._find_closest_building(buildings, player_pos)

        if closest_building['position'] == 'left':
            return 'right_swing'
        elif closest_building['position'] == 'right':
            return 'left_swing'
        else:
            return 'forward_swing'
```

## 🎯 Performance Optimization

### **Frame Rate Optimization**

- **Target**: 60 FPS processing
- **Method**: Frame skipping and async processing
- **Optimization**: YOLOv11s model size and inference speed

### **Memory Management**

- **Streaming**: Process frames without storing full video
- **Cleanup**: Automatic garbage collection of detection results
- **Caching**: Reuse model predictions for similar frames

### **CPU/GPU Utilization**

```python
# GPU acceleration for YOLO
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO('yolov11s.pt').to(device)
```

## 🚦 Safety and Fallbacks

### **Error Handling**

- **Model Loading**: Fallback to basic edge detection
- **Detection Failures**: Default to manual swing patterns
- **Performance Issues**: Automatic quality reduction

### **User Control**

- **Manual Override**: Always allow manual control
- **Toggle System**: Easy on/off for auto-swinging
- **Sensitivity Settings**: Adjustable detection thresholds

## 📈 Expected Performance

### **Detection Accuracy**

- **Buildings**: 90-95% detection rate
- **False Positives**: <5% in game environments
- **Response Time**: <50ms from detection to swing execution

### **Gameplay Impact**

- **Fluid Movement**: Seamless integration with existing controls
- **Natural Swinging**: Realistic swing patterns around obstacles
- **Performance**: No noticeable FPS impact

## 🔮 Future Enhancements

### **Advanced Features**

- **Multi-Building Navigation**: Complex obstacle courses
- **Landmark Recognition**: Special swinging around iconic buildings
- **Weather Adaptation**: Adjust swinging for different conditions
- **Learning System**: Improve detection over time

### **Integration Possibilities**

- **Combat Integration**: Auto-swing during combat
- **Mission Navigation**: Automated traversal to objectives
- **Photo Mode**: Intelligent camera positioning for screenshots

## 🛡️ Technical Considerations

### **Model Requirements**

- **Minimum RAM**: 4GB for YOLOv11s
- **GPU**: Optional but recommended (2GB VRAM)
- **CPU**: Modern multi-core processor

### **Game Compatibility**

- **Windowed Mode**: Required for screen capture
- **Resolution**: Works with any resolution (optimized for 1080p+)
- **Performance**: Minimal impact on game FPS

## 📝 Usage Example

```python
# Initialize the auto-swing system
auto_swing = YOLOAutoSwing()

# Start automated swinging
auto_swing.start()

# The system will now:
# 1. Continuously detect buildings
# 2. Plan optimal swing paths
# 3. Execute web-swing combos automatically
# 4. Navigate around obstacles intelligently

# Stop when needed
auto_swing.stop()
```

This system will transform Spider-Man: Miles Morales into an intelligent, autonomous swinging experience where the AI seamlessly navigates the urban environment!
