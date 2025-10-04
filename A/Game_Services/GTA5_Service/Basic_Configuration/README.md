# GTA5 Player Basic Movement

This folder contains the implementation of basic player movement controls for GTA5 using vgamepad.

## Files

- **`forward_movement.py`** - Main implementation of forward movement controls
- **`test_forward.py`** - Simple test script for forward movement
- **`Basic_Movement_Implementation.md`** - Detailed implementation plan and specifications

## Quick Start

### 1. Prerequisites

Make sure you have:

- ✅ Windows 10/11
- ✅ Python 3.7+
- ✅ ViGEm driver installed
- ✅ vgamepad library installed
- ✅ GTA5 running

### 2. Installation

```bash
# Install dependencies
pip install vgamepad

# Or install all requirements
pip install -r ../requirements.txt
```

### 3. Running the Scripts

#### Option 1: Full Interactive Menu

```bash
python forward_movement.py
```

#### Option 2: Quick Test

```bash
python test_forward.py quick
```

#### Option 3: Interactive Test

```bash
python test_forward.py
```

## Available Commands

### Forward Movement

- **Walk Forward (Normal)** - 60% stick pressure
- **Walk Forward (Slow)** - 30% stick pressure
- **Walk Forward (Fast)** - 90% stick pressure
- **Run Forward** - 100% stick pressure
- **Sprint Forward** - 100% stick pressure + A button

### Control Commands

- **Stop** - Release all inputs
- **Test All Movements** - Run through all movement variations

## How It Works

### Controller Input Mapping

- **Left Stick Forward** → Character moves forward
- **A Button** → Sprint/run modifier
- **Stick Pressure** → Movement speed (30%-100%)

### Human-like Input Patterns

- Random delays between inputs (0.05-0.15s)
- Variable input timing
- Natural movement patterns
- Post-movement delays

## Testing in GTA5

1. **Launch GTA5** and load into a game
2. **Run the script** in a separate terminal
3. **Select movement commands** from the menu
4. **Watch your character** move forward in-game
5. **Test different speeds** to see the variations

## Troubleshooting

### Common Issues

#### "Failed to initialize vgamepad"

- **Solution**: Install ViGEm driver from [ViGEm GitHub](https://github.com/ViGEm/ViGEmBus/releases)
- **Restart** your computer after installation

#### "Controller creation failed"

- **Check**: ViGEm driver is running
- **Verify**: No other virtual controllers are active
- **Restart**: ViGEm service if needed

#### "No movement in GTA5"

- **Verify**: GTA5 has controller support enabled
- **Check**: Controller settings in GTA5
- **Test**: With a real Xbox controller first

### Debug Mode

Add debug output by modifying the script:

```python
# Add this to see detailed input values
print(f"Stick values: X={x_value}, Y={y_value}")
```

## Next Steps

1. **Test all movement commands** in GTA5
2. **Verify input responsiveness** and timing
3. **Check for detection issues** (should be none)
4. **Move to next phase**: Camera controls and other movements

## Success Criteria

- ✅ Character moves forward when commanded
- ✅ Different speeds work correctly
- ✅ Sprint function works (A button + forward)
- ✅ No detection warnings in GTA5
- ✅ Controller appears as legitimate Xbox controller
- ✅ Input timing feels natural

---

_For detailed implementation specifications, see `Basic_Movement_Implementation.md`_
