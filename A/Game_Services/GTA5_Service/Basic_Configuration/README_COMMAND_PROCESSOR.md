# GTA5 Command Processor - Complete Workflow

## 🎯 **MAIN SCRIPT: `command_processor.py`**

This is the **primary script** that solves all your integration questions:

### ✅ **Command Input System**

- **Real-time command processing** - Type commands while GTA5 is running
- **Interactive terminal interface** - Simple text-based commands
- **Command validation** - Checks for valid commands before execution

### ✅ **Window Focus Management**

- **Automatic GTA5 detection** - Finds GTA5 window automatically
- **Auto-refocus before commands** - Brings GTA5 to front before each command
- **Handles minimized windows** - Restores GTA5 if minimized
- **Focus verification** - Ensures GTA5 is active before sending inputs

### ✅ **VgamePad Integration**

- **Seamless controller creation** - Creates virtual Xbox controller
- **Direct input mapping** - Commands → Controller actions
- **Human-like timing** - Natural input patterns
- **Error handling** - Graceful failure recovery

---

## 🚀 **Complete Workflow**

### **Step 1: Setup**

```bash
# Install dependencies
pip install -r ../requirements.txt

# Or use the batch file
launch_command_processor.bat
```

### **Step 2: Launch GTA5**

1. **Start GTA5** and load into a game
2. **Make sure controller support** is enabled in GTA5 settings

### **Step 3: Run Command Processor**

```bash
python command_processor.py
```

### **Step 4: Use Commands**

```
GTA5> walk forward
GTA5> run forward
GTA5> sprint forward
GTA5> look left
GTA5> jump
GTA5> stop
GTA5> help
GTA5> exit
```

---

## 🔧 **How It Solves Your Questions**

### **Q: "How will I input commands?"**

**A: Real-time terminal interface**

- Type commands directly in the terminal
- Commands are processed immediately
- No need to switch between applications

### **Q: "How will it connect to vgamepad?"**

**A: Automatic integration**

- Creates virtual Xbox controller on startup
- Maps commands to controller actions
- Sends inputs directly to GTA5

### **Q: "How will it be sent to move the player?"**

**A: Direct controller input**

- Commands → Controller stick movements
- GTA5 receives input as legitimate controller
- Character moves immediately

### **Q: "How will it refocus GTA5?"**

**A: Automatic window management**

- Detects GTA5 window automatically
- Brings GTA5 to front before each command
- Handles minimized/background windows

---

## 📋 **Available Commands**

### **Movement Commands**

- `walk forward` - Normal speed forward
- `walk backward` - Normal speed backward
- `walk left` - Move left
- `walk right` - Move right
- `run forward` - Full speed forward
- `sprint forward` - Sprint with A button

### **Speed Variations**

- `slow walk forward` - 30% speed
- `normal walk forward` - 60% speed
- `fast walk forward` - 90% speed

### **Camera Commands**

- `look left` - Camera left
- `look right` - Camera right
- `look up` - Camera up
- `look down` - Camera down
- `center camera` - Reset camera

### **Action Commands**

- `jump` - Jump with X button
- `crouch` - Crouch with B button
- `stop` - Stop all movement

### **System Commands**

- `focus gta5` - Manually focus GTA5
- `refocus` - Same as focus gta5
- `help` - Show all commands
- `exit` - Quit the program

---

## 🎮 **Example Usage Session**

```
🎮 GTA5 Command Processor
========================================
✅ VgamePad controller initialized
✅ Found GTA5 window: Grand Theft Auto V
🎮 GTA5 Command Processor Ready!

GTA5> walk forward
🎯 Refocusing GTA5 before command...
🎯 GTA5 window focused
🚶 Walking forward (speed: 0.6, duration: 1.0s)
🎯 Moving stick: X=0, Y=19660 for 1.0s
✅ Movement completed

GTA5> sprint forward
🎯 Refocusing GTA5 before command...
🎯 GTA5 window focused
💨 Sprinting forward (duration: 2.0s)
✅ Sprint completed

GTA5> look left
🎯 Refocusing GTA5 before command...
🎯 GTA5 window focused
👀 Looking left (sensitivity: 0.8)
📷 Moving camera: X=-26213, Y=0 for 0.5s
✅ Camera movement completed

GTA5> stop
🛑 Stopping all movement
✅ Stopped

GTA5> exit
👋 Goodbye!
```

---

## 🔍 **Technical Details**

### **Window Management**

- Uses `win32gui` to find and focus GTA5
- Handles window restoration and focus
- Verifies focus before sending inputs

### **Controller Integration**

- Creates `vg.VX360Gamepad()` instance
- Maps commands to stick movements and button presses
- Sends inputs with human-like timing

### **Command Processing**

- Real-time command parsing
- Command validation and error handling
- Automatic GTA5 refocusing

### **Error Handling**

- Graceful failure recovery
- Clear error messages
- Automatic retry logic

---

## 🚀 **Quick Start Commands**

```bash
# Option 1: Use batch file (easiest)
launch_command_processor.bat

# Option 2: Direct Python
python command_processor.py

# Option 3: Install dependencies first
pip install -r ../requirements.txt
python command_processor.py
```

---

## ✅ **Success Criteria**

- ✅ **Commands work in real-time** while GTA5 is running
- ✅ **GTA5 automatically refocuses** before each command
- ✅ **Character moves immediately** when commanded
- ✅ **No detection issues** - appears as legitimate controller
- ✅ **Smooth integration** between command input and game action

---

**This solves all your integration questions and provides a complete, working system for GTA5 automation!**
