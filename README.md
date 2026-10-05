# Space Invaders 👾

A simple recreation of the classic **Space Invaders** arcade game, built with **Python** and **Pygame**.

This project was created as a small hands-on programming exercise focused on game logic, collision detection, object movement, and basic state management.

## Features

- Classic 5 × 11 alien formation
- One player shot on screen at a time
- Alien return fire
- 3 player lives
- Destructible barriers
- Increasing alien speed as enemies are eliminated
- Different alien types with different point values
- Score system
- Explosion effects
- Win state
- Game-over state
- Restart system

## Controls

- `A` — move left
- `D` — move right
- `SPACE` — shoot
- `R` — restart after winning or losing

## Scoring

Different alien rows award different points:

- Top row: **30 points**
- Middle rows: **20 points**
- Bottom rows: **10 points**

## How the Game Works

The alien formation moves horizontally across the screen.

When it reaches an edge, it:

1. reverses direction
2. moves downward

As more aliens are destroyed, the remaining formation moves faster.

The player loses a life when hit by an alien projectile.

The game ends when:

- all 3 lives are lost, or
- the aliens descend past the invasion line

You win by destroying all 55 aliens.

## Barriers

Four defensive barriers sit between the player and the alien formation.

The barriers are made of small individual blocks rather than using a single health value.

Both player and alien projectiles can destroy these blocks, gradually creating holes in the barriers during the game.

## Installation

Make sure Python is installed.

Then install Pygame Community Edition:

```bash
python -m pip install pygame-ce
