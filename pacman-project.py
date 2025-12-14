import pygame
import random
from collections import deque

# --------- Setup ---------
pygame.init()
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Clone")

# --------- Colors ---------
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)

# --------- Game Variables ---------
CELL_SIZE = 30
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Player
player_x, player_y = 1, 1
score = 0

# Ghosts
ghosts = [(COLS-2, ROWS-2), (1, ROWS-2), (COLS-2, 1)]  # red, pink, cyan

# Directions
dx, dy = 0, 0

# --------- Map Generation ---------
def generate_map():
    MAP = [[2]*COLS for _ in range(ROWS)]
    # Borders
    for i in range(ROWS):
        MAP[i][0] = MAP[i][COLS-1] = 1
    for j in range(COLS):
        MAP[0][j] = MAP[ROWS-1][j] = 1

    # Random walls
    attempts = 0
    while attempts < 60:
        x, y = random.randint(1, COLS-2), random.randint(1, ROWS-2)
        if (x, y) in [(player_x, player_y)] + ghosts:
            continue
        MAP[y][x] = 1
        if not is_progressable(MAP):
            MAP[y][x] = 2  # undo wall if it blocks progress
        attempts += 1

    return MAP

# Check if map is still playable using BFS
def is_progressable(MAP):
    visited = [[False]*COLS for _ in range(ROWS)]
    queue = deque([(player_x, player_y)])
    visited[player_y][player_x] = True

    while queue:
        x, y = queue.popleft()
        for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if 0 <= nx < COLS and 0 <= ny < ROWS and not visited[ny][nx] and MAP[ny][nx] != 1:
                visited[ny][nx] = True
                queue.append((nx, ny))

    for y in range(ROWS):
        for x in range(COLS):
            if MAP[y][x] == 2 and not visited[y][x]:
                return False
    return True

MAP = generate_map()

# --------- Functions ---------
def draw_window():
    WIN.fill(BLACK)
    for y, row in enumerate(MAP):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 1:
                pygame.draw.rect(WIN, BLUE, rect)
            elif cell == 2:
                pygame.draw.circle(WIN, WHITE, rect.center, 5)

    # Draw player
    pygame.draw.circle(WIN, YELLOW, (player_x*CELL_SIZE + CELL_SIZE//2, player_y*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2 - 2)

    # Draw ghosts
    colors = [RED, PINK, CYAN]
    for i, (gx, gy) in enumerate(ghosts):
        pygame.draw.circle(WIN, colors[i], (gx*CELL_SIZE + CELL_SIZE//2, gy*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2 - 2)

    pygame.display.update()

def move_player():
    global player_x, player_y, score
    new_x = player_x + dx
    new_y = player_y + dy
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and MAP[new_y][new_x] != 1:
        player_x, player_y = new_x, new_y
        if MAP[player_y][player_x] == 2:
            MAP[player_y][player_x] = 0
            score += 1

def move_ghosts():
    for i, (gx, gy) in enumerate(ghosts):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(directions)
        for dxg, dyg in directions:
            new_x, new_y = gx + dxg, gy + dyg
            if 0 <= new_x < COLS and 0 <= new_y < ROWS and MAP[new_y][new_x] != 1:
                ghosts[i] = (new_x, new_y)
                break

# --------- Main Loop ---------
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx, dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = 1, 0
            elif event.key == pygame.K_UP:
                dx, dy = 0, -1
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, 1
    
    move_player()
    move_ghosts()
    draw_window()
    
    if any(player_x == gx and player_y == gy for gx, gy in ghosts):
        print("Game Over! Score:", score)
        run = False

pygame.quit()
