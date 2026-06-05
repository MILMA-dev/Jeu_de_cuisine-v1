
# Cooking Adventure Clone (Python & Panda3D)

A functional 3D cooking game prototype featuring stylized low-poly graphics, multiple stations, and an order management system.

## Features
- **3D Graphics**: Built using stylized primitive assemblies for a clean, low-poly look.
- **Gameplay Mechanics**:
  - Ingredient crates (Tomato, Onion, Meat).
  - Cutting boards for preparation.
  - Stoves for cooking (with burning and fire mechanics).
  - Trash bin for waste management.
  - Fire extinguisher for emergencies.
  - Plate assembly and serving counter.
- **Customer AI**: Customers arrive, place orders from various categories (Starter, Main, Dessert), and wait at tables.
- **UI & Configuration**:
  - Main menu and Options menu.
  - **Full Keyboard Customization**: Supports AZERTY (ZQSD) and QWERTY.
  - Timer and Score tracking.

## Requirements
- Python 3.x
- Panda3D
- panda3d-simplepbr

Install dependencies:
```bash
pip install panda3d panda3d-simplepbr
```

## How to Play
1. Run `python main.py`.
2. Use **ZQSD** (default) or your custom keys to move.
3. Use **E** (default) to interact with stations.
4. Prepare ingredients as requested by customers and serve them on a plate at the counter.

## Note for VS Code Users
If you see import errors for `panda3d.core`, it's likely because the Panda3D stubs are not being picked up. You can usually ignore this if the game runs correctly, or install `panda3d-stubs` to help the language server:
```bash
pip install panda3d-stubs
```
In `settings.json`, you might also need to add:
```json
"python.analysis.extraPaths": ["./"]
```
