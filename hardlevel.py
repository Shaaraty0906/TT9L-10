import os
import pygame
import random

# Directory path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Size and background color
SCREEN_SIZE = 600
BACKGROUND_COLOR = (255, 255, 255)
PAUSE_BUTTON_COLOR = (200, 200, 200)
PAUSE_BUTTON_HOVER_COLOR = (170, 170, 170)
EXIT_BUTTON_COLOR = (255, 100, 100)
EXIT_BUTTON_HOVER_COLOR = (255, 70, 70)
PAUSE_BUTTON_RECT = pygame.Rect(500, 10, 80, 40)

def load_image(image_path, grid_size):
    image = pygame.image.load(image_path)
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

def draw_grid(screen, tiles, grid_size, tile_order):
    tile_width = SCREEN_SIZE // grid_size
    tile_height = SCREEN_SIZE // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            tile_index = tile_order[index]
            if tile_index != len(tile_order) - 1:
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