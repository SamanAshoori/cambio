# Cambio Card Game Environment

This repository contains a Python implementation of the card game "Cambio". The primary goal of this project is to build a robust game engine that will serve as a custom training environment for a Neural Network using PyTorch.

This code is being developed as part of a semi-serious tutorial series documenting the process of building a game environment and applying Machine Learning concepts from scratch.


## Project Overview

Cambio is a memory and strategy card game played with a standard deck (and jokers). The objective is to achieve the lowest possible score by swapping, peeking at, and shedding cards.

This project is currently in the early stages of development. The focus is on:
1.  Accurately modelling the deck and card logic.
2.  Implementing the specific rules of Cambio (peeking, swapping, sticking).
3.  Creating an interface compatible with Reinforcement Learning agents.

## Current Functionality

As of the latest commit, the `Cambio` class supports:
-   **Deck Initialisation:** Generates a standard 52-card deck.
-   **Seeded Randomisation:** Uses `datetime` to seed the random number generator for reproducible shuffling.
-   **Card Conversion:** Translates integer values (0-51) into human-readable formats (Suit and Rank).
-   **Player Setup:** Basic methods to assign hands to players.

## Prerequisites

-   Python 3.x
-   (Future) PyTorch


## Resources & Inspiration

-   **Game Rules:** [Cambio Card Game Rules](https://cambiocardgame.com/)
-   **Project Inspiration:** [Neural Network concepts](https://www.youtube.com/watch?v=75FnxGTQB7g)

## Note

This project is a learning exercise. The code is written live and may be refactored as the complexity of the AI requirements increases.
