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

def easy_level(screen):
    grid_size = 4
    image_path = 'dog.jpg'
    tiles = load_image(image_path, grid_size)
    tile_order = list(range(len(tiles)))
    shuffle_tiles(tile_order, grid_size)

    start_ticks = pygame.time.get_ticks()
    paused = False
    pause_start_ticks = 0

    dragging = False
    dragged_tile_index = -1

        running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if PAUSE_BUTTON_RECT.collidepoint(mouse_pos):
                    if paused:
                        paused = False
                        start_ticks += pygame.time.get_ticks() - pause_start_ticks
                    else:
                        paused = True
                        pause_start_ticks = pygame.time.get_ticks()
                elif EXIT_BUTTON_RECT.collidepoint(mouse_pos):
                    running = False
                elif not paused:
                    tile_width = SCREEN_SIZE // grid_size
                    tile_height = SCREEN_SIZE // grid_size
                    for i in range(grid_size):
                        for j in range(grid_size):
                            rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
                            if rect.collidepoint(mouse_pos):
                                dragged_tile_index = i * grid_size + j
                                if tile_order[dragged_tile_index] != len(tile_order) - 1:  # Don't drag the empty tile
                                    dragging = True
                                break
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                tile_width = SCREEN_SIZE // grid_size
                tile_height = SCREEN_SIZE // grid_size
                mouse_pos = event.pos
                empty_index = get_empty_index(tile_order)
                empty_rect = pygame.Rect((empty_index % grid_size) * tile_width, (empty_index // grid_size) * tile_height, tile_width, tile_height)
                if empty_rect.collidepoint(mouse_pos):
                    swap(tile_order, dragged_tile_index, empty_index)
                dragged_tile_index = -1

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, tiles, grid_size, tile_order)

        if not paused:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)

        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
        screen.blit(timer_text, (10, 10))


