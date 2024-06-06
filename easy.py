import os
import pygame
import random

#directory path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#size and bg clour
SCREEN_SIZE = 600
BACKGROUND_COLOR = (255, 255, 255)
PAUSE_BUTTON_COLOR = (200, 200, 200)
PAUSE_BUTTON_HOVER_COLOR = (170, 170, 170)
PAUSE_BUTTON_RECT = pygame.Rect(500, 10, 80, 40)

def load_image(image_path, grid_size):
    image = pygame.image.load('bull.jpg')
    image = pygame.transform.scale(image, (SCREEN_SIZE, SCREEN_SIZE))
    tiles = []
    tile_width = SCREEN_SIZE // grid_size
    tile_height = SCREEN_SIZE // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
            tile_image = image.subsurface(rect).copy()
            tiles.append(tile_image)
    return tiles

def get_empty_index(tile_order):
    return tile_order.index(len(tile_order) - 1)

def swap(tile_order, index1, index2):
    tile_order[index1], tile_order[index2] = tile_order[index2], tile_order[index1]

def draw_grid(tiles, grid_size, tile_order):
    tile_width = SCREEN_SIZE // grid_size
    tile_height = SCREEN_SIZE // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            tile_index = tile_order[index]
            if tile_index != len(tile_order) - 1:  # Don't draw the empty tile
                screen.blit(tiles[tile_index], (j * tile_width, i * tile_height))

def is_solved(tile_order):
    return tile_order == list(range(len(tile_order)))

def shuffle_tiles(tile_order, grid_size):
    for _ in range(1000):
        empty_index = get_empty_index(tile_order)
        neighbors = []
        if empty_index % grid_size > 0:
            neighbors.append(empty_index - 1)
        if empty_index % grid_size < grid_size - 1:
            neighbors.append(empty_index + 1)
        if empty_index // grid_size > 0:
            neighbors.append(empty_index - grid_size)
        if empty_index // grid_size < grid_size - 1:
            neighbors.append(empty_index + grid_size)
        swap(tile_order, empty_index, random.choice(neighbors))

def easy_level():
    grid_size = 2
    # Update this path to the actual path where 'bull.jpg' is located
    image_path = 'C:/Users/shaar/Downloads/bull.jpg'
    tiles = load_image(image_path, grid_size)
    tile_order = list(range(len(tiles)))
    random.shuffle(tile_order)
    
    empty_tile = tile_order.index(len(tiles) - 1)
    tile_order[empty_tile], tile_order[-1] = tile_order[-1], tile_order[empty_tile]

#TIMER
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                empty_index = get_empty_index(tile_order)
                if event.key == pygame.K_UP and empty_index + grid_size < len(tile_order):
                    swap(tile_order, empty_index, empty_index + grid_size)
                elif event.key == pygame.K_DOWN and empty_index - grid_size >= 0:
                    swap(tile_order, empty_index, empty_index - grid_size)
                elif event.key == pygame.K_LEFT and (empty_index % grid_size) < grid_size - 1:
                    swap(tile_order, empty_index, empty_index + 1)
                elif event.key == pygame.K_RIGHT and (empty_index % grid_size) > 0:
                    swap(tile_order, empty_index, empty_index - 1)

        screen.fill(BACKGROUND_COLOR)
        draw_grid(tiles, grid_size, tile_order)
        pygame.display.flip()

        if is_solved(tile_order):
            print("Puzzle Solved!")
            running = False

    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Sliding Puzzle")
    easy_level()