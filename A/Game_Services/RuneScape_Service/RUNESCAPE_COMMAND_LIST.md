# Old School RuneScape Command List

## 🎮 **OSRS Automation Commands**

| Command         | Duration   | Description                               | YOLO Detection          |
| --------------- | ---------- | ----------------------------------------- | ----------------------- |
| `chop tree`     | ~3-5s      | Chop nearest tree (Woodcutting)           | Tree detection          |
| `chop oak`      | ~3-5s      | Chop oak tree specifically                | Oak tree detection      |
| `chop willow`   | ~3-5s      | Chop willow tree specifically             | Willow tree detection   |
| `chop maple`    | ~3-5s      | Chop maple tree specifically              | Maple tree detection    |
| `chop yew`      | ~3-5s      | Chop yew tree specifically                | Yew tree detection      |
| `chop magic`    | ~3-5s      | Chop magic tree specifically              | Magic tree detection    |
| `mine rock`     | ~5-8s      | Mine nearest rock (Mining)                | Rock detection          |
| `mine iron`     | ~5-8s      | Mine iron rock specifically               | Iron rock detection     |
| `mine coal`     | ~5-8s      | Mine coal rock specifically               | Coal rock detection     |
| `attack goblin` | ~2-4s      | Attack goblin NPC (Combat)                | Goblin detection        |
| `attack cow`    | ~2-4s      | Attack cow NPC (Combat)                   | Cow detection           |
| `chick`         | ~2-4s      | Attack chicken NPC (Combat)               | Chicken detection       |
| `chick hunting` | Continuous | Continuous chicken hunting (7s intervals) | Chicken detection       |
| `end`           | Instant    | Stop continuous chicken hunting           | None                    |
| `collect coins` | ~1s        | Collect coins from ground                 | Coin detection          |
| `open bank`     | ~2s        | Open bank interface                       | Bank building detection |
| `scan objects`  | ~1s        | Scan and show all detected objects        | All objects             |

## 🔄 **Interface Commands**

| Command         | Duration | Description                   | Key Used |
| --------------- | -------- | ----------------------------- | -------- |
| `combat tab`    | Instant  | Switch to Combat interface    | F1       |
| `skills tab`    | Instant  | Switch to Skills interface    | F2       |
| `quests tab`    | Instant  | Switch to Quests interface    | F3       |
| `equipment tab` | Instant  | Switch to Equipment interface | F4       |
| `prayers tab`   | Instant  | Switch to Prayers interface   | F5       |
| `spells tab`    | Instant  | Switch to Spell book          | F6       |
| `inventory tab` | Instant  | Switch to Inventory interface | Esc      |
| `world map`     | Instant  | Open World Map                | Ctrl+M   |

## 🤖 **Automated Activities**

| Command            | Duration | Description                                              |
| ------------------ | -------- | -------------------------------------------------------- |
| `auto woodcut`     | 5-30 min | Enhanced automated woodcutting with inventory management |
| `auto chop oak`    | 5-30 min | Automated oak chopping with tree rotation                |
| `auto chop willow` | 5-30 min | Automated willow chopping with inventory checks          |
| `auto mine`        | 5-30 min | Automated mining loop                                    |
| `auto mine iron`   | 5-30 min | Automated iron mining                                    |

### **Enhanced Auto-Woodcutting Features:**

- **Inventory Management**: Automatically handles full inventory by dropping logs
- **Tree Rotation**: Switches between different tree types for variety
- **Failure Recovery**: Handles consecutive failures with area scanning
- **Human-like Behavior**: Random breaks and realistic timing
- **Axe Validation**: Checks and equips axes from inventory

## 🎯 **YOLO Object Detection**

### **Detected Object Categories:**

- **Trees**: Regular trees, Oak, Willow, Maple, Yew, Magic
- **Rocks**: Tin, Copper, Iron, Coal, Gold, Mithril
- **NPCs**: Goblins, Cows, Chickens, Rats, Spiders
- **Items**: Coins, Potions, Food, Weapons, Tools
- **Buildings**: Banks, Shops, Altars, Furnaces, Anvils

### **Detection Features:**

- **Real-time object detection** using YOLOv8
- **Coordinate mapping** from game to screen coordinates
- **Confidence thresholds** for accurate detection
- **Human-like clicking** with random offsets and timing
- **Debug image saving** for troubleshooting

## ⌨️ **OSRS Key Mappings**

| Key    | Function                           |
| ------ | ---------------------------------- |
| F1-F12 | Interface tabs                     |
| Esc    | Inventory tab / Close interface    |
| Tab    | Reply to private message           |
| Space  | Continue dialogue / Make-X default |
| 1-5    | Dialogue response options          |
| Ctrl+M | Open World Map                     |

## 🖱️ **Mouse Controls**

- **Left-click**: Primary interaction (chop, mine, attack)
- **Right-click**: Context menu (not implemented yet)
- **Human-like movement**: Gradual cursor movement with random offsets
- **Smart timing**: Random delays between actions

## 📊 **Usage Examples**

```
Game> chop tree
🌳 Starting woodcutting - looking for tree...
🔍 Checking equipment for axe...
🔍 Searching for tree...
🎯 Found closest tree: tree at (456, 234)
🖱️ Clicked at (456, 234) with left button
✅ Started chopping tree
🪓 Confirmed chopping animation active

Game> chop oak
🌳 Looking for oak tree...
🔍 Searching for oak tree...
🎯 Found closest oak tree: oak tree at (512, 198)
🖱️ Clicked at (512, 198) with left button
✅ Started chopping oak tree

Game> auto woodcut 10
🌳 Starting enhanced auto-woodcutting for 10 minutes...
📋 Settings: tree_type=tree, inventory_check=True, tree_rotation=True
🔍 Checking equipment for axe...
✅ Successfully chopping tree
⏳ Chopping for 6.2 seconds...
🔄 Rotating to next tree type...
📦 Inventory is full! Dropping logs or banking...
🗑️ Dropping logs to make space...
✅ Inventory space cleared
(continues for 10 minutes with enhanced features)

Game> scan objects
🔍 Scanning for all objects...
📊 Scan complete - Found 15 objects:
   tree: 3 objects
   rock: 2 objects
   person: 1 objects
   item: 4 objects
💾 Saved debug image: runescape_scan.png
```

## ⚠️ **Important Notes**

- **YOLO Detection**: Requires YOLOv8 model (yolov8n.pt)
- **Game Window**: Must have OSRS window open and visible
- **Object Recognition**: Based on general YOLO classes, may need custom training
- **Human-like Behavior**: Includes random delays and movements
- **Debug Mode**: Saves detection images for troubleshooting
