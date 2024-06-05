import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the puzzle
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 5, 5
TILE_SIZE = WIDTH // COLS

# Load the image
image = pygame.image.load("TT9L-10\BLUELION.jpg")
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

# Split the image into tiles
tiles = []
for i in range(ROWS):
    for j in range(COLS):
        tile = image.subsurface((j * TILE_SIZE, i * TILE_SIZE,i * TILE_SIZE,TILE_SIZE,TILE_SIZE))
        tiles.append(tile)

#Create a list to keep track of the tile positions
tile_positions = list(range(ROWS * COLS))
empty_tile_index = ROWS * COLS - 1
Tile_positions[empty_tile_index] = None

# Shuffle the tiles, except the last one
random.shuffle(tile_positions[:-1])


# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Slide Puzzle')

def is_adjacent(index1, index2):
    row1, col1 = divmod(index1, COLS)
    row2, col2 = divmod(index2, COLS)
    return abs(row1 - row2) + abs(col1 - col2) == 1

# Game variables
empty_tile_index = ROWS * COLS - 1
game_over = False

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            tile_index = (y // (HEIGHT // ROWS)) * COLS + x // (WIDTH // COLS)
            if abs(tile_index - empty_tile_index) in [1, COLS] and 0 <= tile_index < ROWS * COLS:
                tiles[empty_tile_index], tiles[tile_index] = tiles[tile_index], tiles[empty_tile_index]
                empty_tile_index = tile_index

    # Draw the tiles
    for i, tile in enumerate(tiles):
        x = (i % COLS) * WIDTH // COLS
        y = (i // COLS) * HEIGHT // ROWS
        window.blit(tile, (x, y))

    # Check if the puzzle is solved
    solved = True
    for i in range(ROWS * COLS - 1):
        if tiles[i] != tiles[i + 1] and tiles[i] != tiles[empty_tile_index] and tiles[i + 1] != tiles[empty_tile_index]:
            solved = False
            break
    if solved:
        game_over = True
        print("Congrats, you solved the puzzle!")

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()









































