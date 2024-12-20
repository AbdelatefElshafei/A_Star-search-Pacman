
# AI Pac-Man Game

This repository contains an implementation of an AI-controlled Pac-Man game using Python and Pygame. The game features:

- A grid-based maze with walls and coins.
- A player-controlled Pac-Man that can move in four directions.
- Ghosts that chase Pac-Man using the A* search algorithm.
- Simple graphics rendered using Pygame.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Mechanics](#game-mechanics)
  - [Controls](#controls)
  - [Objective](#objective)
  - [Ghost AI](#ghost-ai)
- [Code Structure](#code-structure)
  - [Imports and Initialization](#imports-and-initialization)
  - [Constants and Global Variables](#constants-and-global-variables)
  - [Game Components](#game-components)
  - [A* Search Algorithm](#a-search-algorithm)
  - [Main Game Loop](#main-game-loop)
  - [Game Over and Restart](#game-over-and-restart)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The AI Pac-Man game is a simple simulation where a player controls Pac-Man in a maze filled with walls and coins. Ghosts move intelligently using the A* search algorithm to chase Pac-Man. The objective is to collect all the coins without being caught by the ghosts.

## Installation
To run the game, ensure you have Python 3 and Pygame installed on your system.

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/ai-pacman-game.git
    ```

2. Install the required packages:

    ```bash
    pip install pygame
    ```

3. Run the game:

    ```bash
    python pacman_game.py
    ```

## How to Play
- Use the arrow keys to move Pac-Man around the maze.
- Collect all the coins while avoiding the ghosts.
- If a ghost catches Pac-Man, the game is over.
- Press 'R' to restart the game after a game over.

## Game Mechanics

### Controls
- Arrow Keys: Move Pac-Man up, down, left, or right.

### Objective
- Collect all coins in the maze.
- Avoid being caught by the ghosts.

### Ghost AI
- Ghosts use the A* search algorithm to find the shortest path to Pac-Man.
- Ghost movements are calculated every few frames to simulate strategic chasing.

## Code Structure

### Imports and Initialization

```python
import pygame
import sys
from queue import PriorityQueue

pygame.init()
```
Import necessary libraries: `pygame` for game development, `sys` for system-specific parameters, and `PriorityQueue` for the A* algorithm.

### Constants and Global Variables

```python
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
SQUARE_SIZE = WIDTH // COLS

# Color definitions
BLACK = (0, 0, 0)      # Background
WHITE = (255, 255, 255)  # Coins
YELLOW = (255, 255, 0)   # Player (Pac-Man)
RED = (255, 0, 0)        # Ghosts
GREEN = (0, 255, 0)      # Walls

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Pac-Man")
```
Set up the game window and define colors and sizes.

### Game Components

#### Walls Definition

```python
walls = [
    (0, 0), (0, 1), (0, 2), ..., (19, 18), (19, 19)
    # Complete list of wall positions
]
```
Define the positions of walls in the maze as a list of `(x, y)` tuples.

#### Player and Ghost Starting Positions

```python
player_start_pos = [1, 1]
ghost_start_positions = [[9, 9], [9, 10], [10, 9], [10, 10]]
```
Set the starting positions for Pac-Man and the ghosts.

### A* Search Algorithm

#### Heuristic Function

```python
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```
Calculate the Manhattan distance between two grid positions.

#### A* Function Implementation

```python
def a_star(start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for node in all_nodes}
    f_score = {node: float('inf') for node in all_nodes}
    g_score[start] = 0
    f_score[start] = heuristic(start, end)

    while not open_set.empty():
        current = open_set.get()[1]
        if current == end:
            return reconstruct_path(came_from, current)
        for neighbor in get_neighbors(current):
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                open_set.put((f_score[neighbor], neighbor))
    return []
```
Implements the A* algorithm to find the shortest path from the ghost to Pac-Man.

### Main Game Loop

```python
def main():
    while True:
        # Initialization
        player_pos = player_start_pos[:]
        ghost_positions = [pos[:] for pos in ghost_start_positions]
        coins = generate_coins()
        
        # Game loop
        while run:
            handle_events()
            update_player_position()
            update_ghost_positions()
            check_collisions()
            render_game()
```
- **Event Handling**: Process user inputs and game events.
- **Player Movement**: Update Pac-Man's position based on user input.
- **Ghost Movement**: Move ghosts towards Pac-Man using the A* algorithm.
- **Collision Detection**: Check for collisions between Pac-Man and ghosts or coins.
- **Rendering**: Draw all game elements on the screen.

### Game Over and Restart

```python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            main()
```
After a game over, allow the player to restart by pressing 'R'.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.
