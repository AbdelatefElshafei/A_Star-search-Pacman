import pygame
import sys
from queue import PriorityQueue

pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
SQUARE_SIZE = WIDTH // COLS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Pac-Man")
walls = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19),
    (1, 0), (1, 19),
    (2, 0),  (2, 11), (2, 12), (2, 13), (2, 19),
    (3, 0), (3, 5), (3, 13), (3, 19),
    (4, 0), (4, 5), (4, 13), (4, 19),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 13), (5, 15), (5, 16), (5, 17), (5, 19),
    (6,0),(6, 3), (6, 11), (6, 15),(6,19),
    (7,0),(7, 3), (7, 11), (7, 15),(7,19),
    (8,0),(8, 3), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 15),(8,19),
    (9,0),(9, 15),(9,19),
    (10,0),(10, 15),(10,19),
    (11, 0), (11, 1), (11, 2), (11, 3), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (11, 13), (11, 15), (11, 16), (11, 17), (11, 19),
    (12, 0), (12, 5), (12, 13), (12, 19),
    (13, 0), (13, 5), (13, 13), (13, 19),
    (14, 0), (14, 5),  (14, 11), (14, 12), (14, 13), (14, 19),
    (15, 0), (15, 19),
    (16, 0), (16, 1), (16, 2), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11),(16,12),(18,12),(19,12),(19,13),(16,19),(17,19),(18,19),
    (17,0),(18,0),(19,0),(19,14),(19,15),(19,16),(19,17),(19,18),(19,19),(19,20)
    ,(19,1),(19,2),(19,3),(19,4),(19,5),(19,6),(19,7),(19,8),(19,9),(19,10),(19,11)
    ]
player_start_pos = [1, 1]
ghost_start_positions = [[9, 9], [9, 10], [10, 9], [10, 10]]
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def a_star(start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for row in range(ROWS) for node in [(row, col) for col in range(COLS)]}
    g_score[start] = 0
    f_score = {node: float('inf') for row in range(ROWS) for node in [(row, col) for col in range(COLS)]}
    f_score[start] = heuristic(start, end)
    while not open_set.empty():
        current = open_set.get()[1]
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and neighbor not in walls:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                    open_set.put((f_score[neighbor], neighbor))
    return []
def main():
    global player_start_pos, ghost_start_positions
    while True:
        player_pos = player_start_pos[:]
        ghost_positions = [pos[:] for pos in ghost_start_positions]
        coins = [(x, y) for x in range(ROWS) for y in range(COLS) if (x, y) not in walls and (x, y) != tuple(player_pos)]
        clock = pygame.time.Clock()
        run = True
        ghost_move_counter = 0
        ghost_move_delay = 10  
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            new_pos = player_pos[:]
            if keys[pygame.K_LEFT]:
                new_pos[0] -= 1
            if keys[pygame.K_RIGHT]:
                new_pos[0] += 1
            if keys[pygame.K_UP]:
                new_pos[1] -= 1
            if keys[pygame.K_DOWN]:
                new_pos[1] += 1
            if tuple(new_pos) not in walls:
                player_pos = new_pos
            if tuple(player_pos) in coins:
                coins.remove(tuple(player_pos))
            if tuple(player_pos) in [tuple(g) for g in ghost_positions]:
                print("Game Over! Press R to try again.")
                run = False
            ghost_paths = []  
            if ghost_move_counter == 0:
                for ghost_pos in ghost_positions:
                    path = a_star(tuple(ghost_pos), tuple(player_pos))
                    ghost_paths.append(path) 
                    if path:
                        ghost_pos[0], ghost_pos[1] = path[0]
            ghost_move_counter = (ghost_move_counter + 1) % ghost_move_delay
            WIN.fill(BLACK)
            for wall in walls:
                pygame.draw.rect(WIN, GREEN, (wall[0] * SQUARE_SIZE, wall[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            for coin in coins:
                pygame.draw.circle(WIN, WHITE, (coin[0] * SQUARE_SIZE + SQUARE_SIZE // 2, coin[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)
            for path in ghost_paths:
                for i in range(1, len(path)):
                    start_pos = (path[i-1][0] * SQUARE_SIZE + SQUARE_SIZE // 2, path[i-1][1] * SQUARE_SIZE + SQUARE_SIZE // 2)
                    end_pos = (path[i][0] * SQUARE_SIZE + SQUARE_SIZE // 2, path[i][1] * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(WIN, RED, start_pos, end_pos, 3)
            pygame.draw.circle(WIN, YELLOW, (player_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2, player_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2)
            for ghost_pos in ghost_positions:
                pygame.draw.circle(WIN, RED, (ghost_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2, ghost_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2)
            pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    main()
if __name__ == "__main__":
    main()