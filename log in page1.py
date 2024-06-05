import pygame
import sys

pygame.init()

# Screen settings
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("loginbackground2.jpg")
BG = pygame.transform.scale(BG, (1280, 720))  # Scale the background image to fit the screen

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)
input_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 60)

# Input boxes
input_boxes = [
    pygame.Rect(540, 250, 200, 50),  # Username box
    pygame.Rect(540, 350, 200, 50)  # Password box
]

# Variables
username = ''
user_password = ''
active_box = None
mode = 'login'
message = ''

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def login(user, pwd):
    global message, mode, username, user_password
    success = False
    with open("logindatabase.txt", "r") as file:
        for line in file:
            a, b = line.strip().split(",")
            if a == user and b == pwd:
                success = True
                break
    if success:
        message = "Login successful!"
    else:
        message = "Invalid credentials. Please register."
        mode = 'register'
        username = ''
        user_password = ''

def register(user, pwd):
    global message
    with open("logindatabase.txt", "a") as file:
        file.write(f"\n{user},{pwd}")
    message = "You have been registered!"

def main():
    global username, user_password, active_box, mode, message

    running = True
    while running:
        SCREEN.blit(BG, (0, 0))
        draw_text('LOGIN PAGE' if mode == 'login' else 'Register Page', font, BLACK, SCREEN, 520, 100)
        draw_text('USERNAME:', input_font, BLACK, SCREEN, 300, 258)
        draw_text('Password:', input_font, WHITE, SCREEN, 340, 350)
        pygame.draw.rect(SCREEN, WHITE if active_box == 0 else GRAY, input_boxes[0], 2)
        pygame.draw.rect(SCREEN, WHITE if active_box == 1 else GRAY, input_boxes[1], 2)
        
        draw_text(username, input_font, BLACK, SCREEN, input_boxes[0].x+5, input_boxes[0].y+5)
        draw_text('*' * len(user_password), input_font, BLACK, SCREEN, input_boxes[1].x+5, input_boxes[1].y+5)

        # Buttons
        login_button = pygame.Rect(490, 500, 150, 60)
        register_button = pygame.Rect(690, 500, 190, 60)
        pygame.draw.rect(SCREEN, BLUE, login_button)
        pygame.draw.rect(SCREEN, BLUE, register_button)
        draw_text('Login', button_font, WHITE, SCREEN, 515, 510)
        draw_text('Register', button_font, WHITE, SCREEN, 695, 510)

        # Display message
        draw_text(message, input_font, RED, SCREEN, 540, 600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_boxes[0].collidepoint(event.pos):
                    active_box = 0
                elif input_boxes[1].collidepoint(event.pos):
                    active_box = 1
                else:
                    active_box = None
                if login_button.collidepoint(event.pos):
                    if mode == 'login':
                        login(username, user_password)
                    else:
                        register(username, user_password)
                elif register_button.collidepoint(event.pos):
                    mode = 'register'
                    username = ''
                    user_password = ''
                    message = ''
            if event.type == pygame.KEYDOWN:
                if active_box == 0:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_box == 1:
                    if event.key == pygame.K_BACKSPACE:
                        user_password = user_password[:-1]
                    else:
                        user_password += event.unicode

        pygame.display.update()

main()
