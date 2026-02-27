# Royal Remedy Run

A 2D platformer game built with **Python** and **Pygame** where you play as a princess navigating through 4 challenging levels filled with enemies, lava traps, and collectible coins — all in search of the Royal Remedy!

---

## Gameplay Preview

| Main Menu                          | In Game                             | Game Over                              |
| ---------------------------------- | ----------------------------------- | -------------------------------------- |
| ![Main Menu](screenshots/menu.png) | ![Gameplay](screenshots/level1.png) | ![Game Over](screenshots/gameover.png) |

---

## Controls

| Key             | Action     |
| --------------- | ---------- |
| `→` Right Arrow | Move right |
| `←` Left Arrow  | Move left  |
| `Space`         | Jump       |

---

## Game Overview

- **4 unique levels**, each with its own background and increasing difficulty
- **3 lives** — lose a life when hitting an enemy or falling in lava
- **Coins** to collect and track your score
- **Gate** at the end of each level to advance to the next
- **Royal Remedy** collectible at the final level — find it to win the game!

---

## Installation & Running

### 1. Clone the repository

```bash
git clone https://github.com/buyakawo/Royal-Remedy-Run.git
cd Royal-Remedy-Run
```

### 2. Install dependencies

```bash
pip install pygame
```

### 3. Run the game

```bash
python main.py
```

---

## Code Architecture

**`globals.py`** — Shared game state accessible across all modules. Tracks `game_over` status (`0` = running, `-1` = game over, `1` = level complete), `player_lives`, and `max_level`.

**`main.py`** — Core game loop. Handles rendering, level loading via `importlib`, score tracking, background switching per level, and all game state transitions (menu → playing → game over → next level → win screen).

**`player.py`** — Manages the princess: keyboard input, gravity simulation, walking animation cycling, and collision detection with platforms, enemies, lava, coins, the gate, and the remedy.

**`enemy.py`** — Animated enemy sprite that cycles through 5 frames at a configurable speed. Triggers a life loss on contact with the player.

**`button.py`** — Reusable clickable UI button using mouse position and click state detection.

**`levels/level*.py`** — Each file exports a `level_data` 2D grid (13 rows × 19 columns) using tile codes.

---

## Built With

- [Python 3](https://www.python.org/)
- [Pygame](https://www.pygame.org/)

---

## Author

Made by [@buyakawo](https://github.com/buyakawo)

---
