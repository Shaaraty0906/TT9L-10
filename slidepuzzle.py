import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the puzzle
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 4, 4

# Load the image
image = pygame.image.load('monalisa.jpg')
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

# Split the image into tiles
tiles = []
for i in range(ROWS):
    for j in range(COLS):
        tile = image.subsurface((j * WIDTH // COLS, i * HEIGHT // ROWS, WIDTH // COLS, HEIGHT // ROWS))
        tiles.append(tile)

# Shuffle the tiles
random.shuffle(tiles)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Slide Puzzle')

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
        print("Congratulations, you solved the puzzle!")

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()









































