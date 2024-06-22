import os
import pygame
import random

# Initialize Pygame
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Constants and settings
SCREEN_SIZE = 600
BACKGROUND_COLOR = (255, 255, 255)
PAUSE_BUTTON_COLOR = (200, 200, 200)
PAUSE_BUTTON_HOVER_COLOR = (170, 170, 170)
EXIT_BUTTON_COLOR = (255, 100, 100)
EXIT_BUTTON_HOVER_COLOR = (255, 70, 70)
PAUSE_BUTTON_RECT = pygame.Rect(500, 10, 80, 40)
EXIT_BUTTON_RECT = pygame.Rect(500, 60, 80, 40)
FONT = pygame.font.Font(None, 36)

def get_empty_index(tile_order):
    return tile_order.index(len(tile_order) - 1)

def swap(tile_order, index1, index2):
    tile_order[index1], tile_order[index2] = tile_order[index2], tile_order[index1]

def draw_grid(tiles, grid_size, tile_order, screen):
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
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    empty_index = get_empty_index(tile_order)
    empty_pos = (empty_index // grid_size, empty_index % grid_size)
    
    for _ in range(random.randint(1, 5)):  
        valid_moves = []
        for move in moves:
            new_pos = (empty_pos[0] + move[0], empty_pos[1] + move[1])
            if 0 <= new_pos[0] < grid_size and 0 <= new_pos[1] < grid_size:
                valid_moves.append(move)
        move = random.choice(valid_moves)
        new_pos = (empty_pos[0] + move[0], empty_pos[1] + move[1])
        new_index = new_pos[0] * grid_size + new_pos[1]
        swap(tile_order, empty_index, new_index)
        empty_pos = new_pos
        empty_index = new_index

def display_message(screen, message):
    screen.fill(BACKGROUND_COLOR)
    text = FONT.render(message, True, (0, 0, 0))
    screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def save_results(time_taken):
    with open('results.py', 'w') as file:
        file.write(f"time_taken = {time_taken}\n")

def medium_level(screen):
    grid_size = 3  
    image_path = 'tiger.jpg'
    
    try:
        tiles = pygame.image.load(image_path)
        tiles = pygame.transform.scale(tiles, (SCREEN_SIZE, SCREEN_SIZE))
        tiles = [tiles.subsurface(pygame.Rect(j * SCREEN_SIZE // grid_size, i * SCREEN_SIZE // grid_size, SCREEN_SIZE // grid_size, SCREEN_SIZE // grid_size)) for i in range(grid_size) for j in range(grid_size)]
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return
    
    tile_order = list(range(len(tiles)))
    shuffle_tiles(tile_order, grid_size) 

    start_ticks = pygame.time.get_ticks()
    paused = False
    pause_start_ticks = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not paused:
                empty_index = get_empty_index(tile_order)
                if event.key == pygame.K_UP and empty_index + grid_size < len(tile_order):
                    swap(tile_order, empty_index, empty_index + grid_size)
                elif event.key == pygame.K_DOWN and empty_index - grid_size >= 0:
                    swap(tile_order, empty_index, empty_index - grid_size)
                elif event.key == pygame.K_LEFT and empty_index % grid_size < grid_size - 1:
                    swap(tile_order, empty_index, empty_index + 1)
                elif event.key == pygame.K_RIGHT and empty_index % grid_size > 0:
                    swap(tile_order, empty_index, empty_index - 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE_BUTTON_RECT.collidepoint(event.pos):
                    if paused:
                        paused = False
                        start_ticks += pygame.time.get_ticks() - pause_start_ticks
                    else:
                        paused = True
                        pause_start_ticks = pygame.time.get_ticks()
                elif EXIT_BUTTON_RECT.collidepoint(event.pos):
                    running = False

        screen.fill(BACKGROUND_COLOR)
        draw_grid(tiles, grid_size, tile_order, screen)

        if not paused:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)

        timer_text = FONT.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
        screen.blit(timer_text, (10, 10))

        mouse_pos = pygame.mouse.get_pos()
        pause_button_color = PAUSE_BUTTON_COLOR if not PAUSE_BUTTON_RECT.collidepoint(mouse_pos) else PAUSE_BUTTON_HOVER_COLOR
        pygame.draw.rect(screen, pause_button_color, PAUSE_BUTTON_RECT)
        pause_text = FONT.render("Pause" if not paused else "Resume", True, (0, 0, 0))
        screen.blit(pause_text, (PAUSE_BUTTON_RECT.x + 5, PAUSE_BUTTON_RECT.y + 5))      

        exit_button_color = EXIT_BUTTON_COLOR if not EXIT_BUTTON_RECT.collidepoint(mouse_pos) else EXIT_BUTTON_HOVER_COLOR
        pygame.draw.rect(screen, exit_button_color, EXIT_BUTTON_RECT)
        exit_text = FONT.render("Exit", True, (0, 0, 0))
        screen.blit(exit_text, (EXIT_BUTTON_RECT.x + 20, EXIT_BUTTON_RECT.y + 5))
        
        if is_solved(tile_order):
            time_taken = (pygame.time.get_ticks() - start_ticks) / 1000
            save_results(time_taken)
            display_message(screen, "Congratulations! Puzzle solved!")
            pygame.time.delay(2000)
            running = False

        pygame.display.flip()

    guessing_game(screen)

def guessing_game(screen):
    guessing = True
    user_guess = ""
    input_box = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2, 200, 50)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False

    while guessing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                guessing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if user_guess.lower() == "tiger":
                            display_message(screen, "Correct! It's a tiger!")
                        else:
                            display_message(screen, "Incorrect! Try again.")
                        pygame.time.delay(2000)
                        guessing = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_guess = user_guess[:-1]
                    else:
                        user_guess += event.unicode
                        input_box.w = max(200, FONT.size(user_guess)[0] + 10)

        screen.fill(BACKGROUND_COLOR)
        prompt_text = FONT.render("Guess the animal in the picture:", True, (0, 0, 0))
        pygame.draw.rect(screen, color, input_box, 2)
        user_input_text = FONT.render(user_guess, True, (0, 0, 0))
        screen.blit(prompt_text, (SCREEN_SIZE // 2 - prompt_text.get_width() // 2, SCREEN_SIZE // 2 - 50))
        screen.blit(user_input_text, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Sliding Puzzle")
    medium_level(screen)

















































