# Cambio AI — Neural Network from Scratch

## What is this project?

This project started as a personal deep dive into how neural networks actually work — not by calling `model.fit()`, but by building every component from scratch in NumPy: forward passes, backpropagation, gradient descent, and a full Q-learning training loop.

The game engine (Cambio) was also built from scratch as a vehicle for the ML work. The Pygame front end was generated with AI assistance — that was intentional, since the focus of the project was the ML implementation, not the GUI.

---

## What I built manually (no PyTorch / TensorFlow)

- A `Neuron` and `Layer` class with matrix multiply forward passes
- Manual backpropagation with the chain rule
- ReLU activation, MSE loss, and gradient descent
- A `Network` class supporting arbitrary depth (e.g. `[19, 64, 64, 6]`)
- A Q-learning agent with epsilon-greedy action selection
- Experience replay buffer (`deque`, capacity 10,000)
- Game state encoding — 19-input vector from partial information
- Dense + terminal reward signal
- Weight persistence with `np.save` / `np.load`

---

## The Cambio Engine

Cambio is a card game where the goal is to have the lowest total score in your hand when someone calls "Cambio." Players have partial information — you only know some of your own cards, and can learn about opponent cards through power cards.

The engine supports:
- 2+ players (human + AI in the GUI, or AI vs AI in training)
- Full power card logic (Peek Self, Peek Opponent, Blind Swap, Single/Double Peek Swap)
- Partial knowledge tracking per player
- Risk tolerance calculated dynamically from known card scores

### Card Values
| Card | Value |
|------|-------|
| Ace | 1 |
| 2–9 | Face value |
| 10, J, Q, K | 10 |
| Red Kings (K♥, K♦) | -1 |
| Joker | 0 |

### Power Cards
| Card | Power |
|------|-------|
| 7, 8 | Peek one of your own unknown cards |
| 9, 10 | Peek one of your opponent's unknown cards |
| Jack | Blind swap — exchange one of your cards with an opponent's |
| Queen | Peek opponent card, then swap |
| King | Peek own + opponent card, then swap |

---

## AI Agents

| Agent | Description |
|-------|-------------|
| **Random** | Picks actions uniformly at random |
| **Heuristic** | Rule-based logic with risk tolerance and card score awareness |
| **Q-Learning** | Trained neural network — 19 inputs, two hidden layers, 6 outputs |

### Training Results
After 10,000 episodes against the heuristic opponent:
- Q-learning agent win rate: **~22%**
- Random baseline win rate: **~17%**

The heuristic opponent plays with partial information (2 cards revealed at start, same as a real game). The 5 percentage point gap over random represents genuine learning under uncertainty.

---

## Project Structure

```
cambio.py        — Game engine
player.py        — Player class with knowledge tracking
agent.py         — Q-learning agent, replay buffer, Network wrapper
network.py       — Neural network (Layer, Network, relu, mse_loss)
train.py         — Training loop
baseline.py      — Random agent baseline for comparison
main.py          — Pygame front end (AI assisted)
model_w*.npy     — Saved network weights
model_b*.npy     — Saved network biases
```

---

## How to Install

**Requirements:** Python 3.10+, NumPy, Pygame

```bash
git clone https://github.com/SamanAshoori/cambio-ai
cd cambio-ai
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install numpy pygame
```

---

## How to Play

### Play the game (human vs AI)
```bash
python main.py
```

On your turn:
- **Click a slot** in your hand to swap the drawn card with that card
- **Discard button** — discard the drawn card without swapping
- **Cambio button** — call Cambio when you think your score is low enough to win

### Train the Q-learning agent
```bash
python train.py
```
Trains for 1,000 episodes by default. Saves weights to `model_w*.npy` automatically on completion. Edit `episodes` in `train.py` to train longer.

### Run the random baseline
```bash
python baseline.py
```

---

## How to Win

Call "Cambio" when you believe your hand score is lower than your opponent's. Your opponent gets one final turn after you call it. Lowest score wins. A draw is possible.

**Strategy tips:**
- You start knowing 2 of your 4 cards — use power cards to learn more
- Red Kings (-1) are the best cards in the game — never swap them away
- Don't call Cambio too early — your opponent might have a lower score than you think

---

## Neural Network Architecture

```
Input (19)  →  Hidden (64)  →  Hidden (64)  →  Output (6)
```

**Input vector (19 values):**
- Own cards: score + known flag × 4 = 8 values
- Opponent cards: score + known flag × 4 = 8 values
- Card in hand score: 1 value
- Top of discard score: 1 value
- Risk tolerance: 1 value

**Output (6 Q-values):**
- Actions 0–3: swap drawn card with inventory slot 0–3
- Action 4: discard drawn card
- Action 5: call Cambio

---

## Acknowledgements

Neural network implementation built incrementally from scratch — single neuron → layer → backprop → Q-learning — as a learning exercise. No ML frameworks were used in the core engine.