import pygame
import sys
import tkinter as tk
from tkinter import messagebox

# Initialize pygame
pygame.init()

# Initialize tkinter root for message boxes
root = tk.Tk()
root.withdraw()  # Hide the root window

# Set up the screen
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("loginbackground2.jpg")
BG = pygame.transform.scale(BG, (1280, 720))  # Scale the background image to fit the screen

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define fonts
font = pygame.font.Font(None, 74)
input_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 60)

# Define input boxes
input_boxes = [
    pygame.Rect(560, 250, 260, 50),
    pygame.Rect(560, 345, 260, 50)
]

username = ''
user_password = ''
active_box = None
message = ''
state = 'login'  # Initial state

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def login(user, pwd):
    global message, state, username, user_password
    username_correct = False
    password_correct = False
    
    with open("logindatabase.txt", "r") as file:
        for line in file:
            a, b = line.strip().split(",")
            if a == user:
                username_correct = True
            if b == pwd:
                password_correct = True
            if a == user and b == pwd:
                message = "Login successful!"
                messagebox.showinfo("Login", message)
                state = 'main_menu'  # Transition to main menu state
                return

    if not username_correct and not password_correct:
        messagebox.showerror("Login Failed", "Incorrect Username and Password")
    elif not username_correct:
        messagebox.showerror("Login Failed", "Incorrect Username")
    elif not password_correct:
        messagebox.showerror("Login Failed", "Incorrect Password")

def register(user, pwd):
    global message, state
    with open("logindatabase.txt", "a") as file:
        file.write(f"\n{user},{pwd}")
    message = "You have been registered!"
    messagebox.showinfo("Register", message)
    state = 'login'  # Return to login state after registration

def login_page():
    global username, user_password, active_box, message, state

    SCREEN.blit(BG, (0, 0))
    draw_text('LOGIN PAGE', font, BLACK, SCREEN, 520, 100)
    draw_text('USERNAME:', input_font, BLACK, SCREEN, 300, 258)
    draw_text('PASSWORD:', input_font, BLACK, SCREEN, 305, 360)
    pygame.draw.rect(SCREEN, WHITE if active_box == 0 else GRAY, input_boxes[0], 2)
    pygame.draw.rect(SCREEN, WHITE if active_box == 1 else GRAY, input_boxes[1], 2)
    
    draw_text(username, input_font, BLACK, SCREEN, input_boxes[0].x+5, input_boxes[0].y+5)
    draw_text('*' * len(user_password), input_font, BLACK, SCREEN, input_boxes[1].x+5, input_boxes[1].y+5)

    login_button = pygame.Rect(500, 500, 150, 60)
    register_button = pygame.Rect(696, 500, 220, 60)
    pygame.draw.rect(SCREEN, WHITE, login_button)
    pygame.draw.rect(SCREEN, WHITE, register_button)
    draw_text('LOGIN', button_font, BLACK, SCREEN, 510, 510)
    draw_text('REGISTER', button_font, BLACK, SCREEN, 700, 510)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                login(username, user_password)
            elif register_button.collidepoint(event.pos):
                state = 'register'
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

def register_page():
    global username, user_password, active_box, message, state

    SCREEN.blit(BG, (0, 0))
    draw_text('REGISTER PAGE', font, BLACK, SCREEN, 520, 100)
    draw_text('USERNAME:', input_font, BLACK, SCREEN, 300, 258)
    draw_text('PASSWORD:', input_font, BLACK, SCREEN, 305, 360)
    pygame.draw.rect(SCREEN, WHITE if active_box == 0 else GRAY, input_boxes[0], 2)
    pygame.draw.rect(SCREEN, WHITE if active_box == 1 else GRAY, input_boxes[1], 2)
    
    draw_text(username, input_font, BLACK, SCREEN, input_boxes[0].x+5, input_boxes[0].y+5)
    draw_text('*' * len(user_password), input_font, BLACK, SCREEN, input_boxes[1].x+5, input_boxes[1].y+5)

    register_button = pygame.Rect(500, 500, 220, 60)
    pygame.draw.rect(SCREEN, WHITE, register_button)
    draw_text('REGISTER', button_font, BLACK, SCREEN, 510, 510)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_boxes[0].collidepoint(event.pos):
                active_box = 0
            elif input_boxes[1].collidepoint(event.pos):
                active_box = 1
            else:
                active_box = None
            if register_button.collidepoint(event.pos):
                register(username, user_password)
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

def main_menu():
    SCREEN.blit(BG, (0, 0))
    draw_text('MAIN MENU', font, BLACK, SCREEN, 520, 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def main():
    global state

    while True:
        if state == 'login':
            login_page()
        elif state == 'register':
            register_page()
        elif state == 'main_menu':
            main_menu()

        pygame.display.update()

main()

