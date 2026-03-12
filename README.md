# Tic Tac Toe with Integrated AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green)
![NumPy](https://img.shields.io/badge/NumPy-2.2.6-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

## 📋 Table of Contents

- [Description](#description)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Project Structure](#project-structure)
- [Features](#features)
- [Results](#results)

---

## 📖 Description

**Tic Tac Toe with Integrated AI** is an interactive Tic Tac Toe application that offers three difficulty levels based on different AI strategies:

- **Easy** : Random moves
- **Medium** : Intelligent heuristic (wins if possible, blocks opponent)
- **Hard** : Q-Learning reinforcement (adaptive learning)

### Use Cases

This project demonstrates:
- ✅ Modular and maintainable architecture
- ✅ Implementation of AI algorithms (Heuristic, Q-Learning)
- ✅ Interactive user interface management
- ✅ Machine Learning with reinforcement
- ✅ Trained model persistence
- ✅ Complex state management

---

## 💻 Installation

### Prerequisites

- Python 3.10 or higher
- pip (package manager)
- macOS / Linux / Windows

### Installation Steps

#### 1. **Access the project directory**

```bash
cd /path/to/TicTacToe
```

#### 2. **Create a virtual environment**

```bash
python3 -m venv tictactoe_venv
```

#### 3. **Activate the virtual environment**

**macOS/Linux** :
```bash
source tictactoe_venv/bin/activate
```

**Windows** :
```bash
tictactoe_venv\Scripts\activate
```

#### 4. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import pygame; import numpy; print('✓ Installation successful')"
```

---

## 🎮 Usage

### Launch the Game

```bash
source tictactoe_venv/bin/activate
python main.py
```

### Usage Flow

```
1. Select your symbol (X or O)
   └─ Press <x> or <o>

2. Choose difficulty
   ├─ <e> Easy (Random moves)
   ├─ <m> Medium (Intelligent heuristic)
   └─ <h> Hard (Q-Learning)

3. [If Hard selected] Manage AI model
   ├─ <l> Load an existing model
   │  └─ Navigate with <↑↓>, select with <Enter>
   ├─ <t> Train a new model
   │  └─ Watch the progress bar
   │  └─ Name the model once trained
   └─ <p> Play with default model

4. Play the Game
   ├─ Click to place your symbol
   ├─ <r> Reset the game
   └─ <Esc> Quit the game
```

### Example: Training an AI

1. Launch the game : `python main.py`
2. Select your symbol
3. Choose **<h>** for Hard (Q-Learning)
4. Choose **<t>** to Train
5. Watch the progress bar (~10-15 minutes for 1M episodes)
6. Enter a name for the model (ex: "my_ai_v1")
7. The model is automatically saved to `QTables/my_ai_v1.pkl`

---

## 🤖 Technical Details

### AI Algorithms

#### **PlayerAI - Heuristic (Medium Difficulty)**

```
Strategy:
  1. Can we win on the next move? → Win
  2. Can the opponent win? → Block
  3. Otherwise → Random move
```

**Time Complexity** : O(n) where n = empty cells  
**Properties** : Never loses against a random AI

#### **QLearningAI - Reinforcement (Hard Difficulty)**

```
Improved Bellman Formula:

Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]

Hyperparameters:
  α = 0.1      (learning rate)
  γ = 0.9      (discount factor)
  ε = 0.9 → 0  (exploration → exploitation)
```

**Training Process** :
1. AI plays 1M games against the heuristic
2. Epsilon decreases linearly over episodes
3. Q-table updated after each action
4. Saved in pickle (Python serialization)

**Advantages** :
- Adaptive learning
- Reusable and improvable models
- Mathematically proven convergence

### State Management

**State Representation** :
- 3x3 NumPy matrix
- Values: 0 (empty), 1 (player), 2 (AI)
- Q-table key: string serializing the state

```python
state = str(board.board.flatten())
# Example: "[[0 1 2 0 1 0 2 0 1]]"
```

### Model Persistence

**Storage Format** :
- **Structure** : Python dictionary `{(state, action): q_value}`
- **Serialization** : Pickle (Python binary format)
- **Directory** : `QTables/`
- **Typical size** : 30-300 kB for 1M training

---

## 📁 Project Structure

```
TicTacToe/
├── main.py                 # Entry point
├── game.py                 # Orchestration & Pygame UI
├── ai.py                   # PlayerAI & QLearningAI classes
├── board.py                # Game board logic
├── constants.py            # UI Configuration & constants
├── requirements.txt        # Project dependencies
├── README.md               # This documentation
├── tictactoe_venv/         # Python virtual environment
├── QTables/                # Trained AI models
│   ├── q_table.pkl         # Default model
│   ├── my_ai_v1.pkl        # Custom user models
│   └── ...
└── __pycache__/            # Python cache (auto-generated)
```

### Main Files Details

| File | Lines | Responsibility |
|------|-------|-----------------|
| `main.py` | ~30 | Pygame initialization, main loop |
| `game.py` | ~650 | Menus, game logic, training, UI rendering |
| `ai.py` | ~220 | AI algorithms, model persistence |
| `board.py` | ~140 | Game state, win verification |
| `constants.py` | ~70 | UI configuration, colors, dimensions |

---

## ✨ Features

### Implemented ✅

- [x] Interactive Pygame graphical interface
- [x] 3 difficulty levels (Easy, Medium, Hard)
- [x] Heuristic algorithm (Medium)
- [x] Q-Learning with epsilon-greedy policy (Hard)
- [x] In-game training with visual progress bar
- [x] Multiple AI model management
- [x] Save and load trained models
- [x] Win detection (rows, columns, diagonals)
- [x] Keyboard and mouse event handling
- [x] Intuitive menu navigation

### Future Improvements 🚀

- [ ] Minimax algorithm with Alpha-Beta Pruning (unbeatable AI)
- [ ] Deep Q-Network (DQN) with neural network
- [ ] Improved self-play (two Q-Learning AIs against each other)
- [ ] Statistics system (win rate, progression)
- [ ] Player profiles (save progression)
- [ ] Theme system (dark mode, color customization)
- [ ] Unit tests (coverage >80%)
- [ ] Alternative CLI interface (command line)
- [ ] Multiplayer network support (online play)

---

## 🔧 Technical Considerations

### Performance

- **Gameplay** : O(1) per action (table lookup)
- **Training** : 10-15 minutes for 1M episodes (M1 Pro)

### Robustness

- ✅ Error handling for missing files
- ✅ User input validation
- ✅ Automatic `QTables/` directory creation
- ✅ Graceful fallback if model missing
- ✅ Pickle exception handling for corrupted models

## 👨‍💻 Author

**Brice Petit**  
Technical Test Easi - March 2026

---

## 📄 License

MIT License - Free for personal and commercial use

---

**Ready to play? Good luck! 🎮**
