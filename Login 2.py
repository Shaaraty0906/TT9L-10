import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Login and Registration System")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 36)

background_image = pygame.image.load("loginbackground2.jpg")
background_image = pygame.transform.scale(background_image, (width, height))
import pygame
import sys
import os
import subprocess

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Registration")

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Paths
USER_DB_FILE = 'logindatabase.txt'  # Adjust to your file path

# Function to load font
def get_font(size):
    return pygame.font.Font("assets/arial.ttf", size)

# Class for buttons
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

# Function to read database
def read_database(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        data = file.readlines()
    return {line.split(':')[0]: line.split(':')[1].strip() for line in data}

# Function to write to database
def write_to_database(file_path, data):
    with open(file_path, 'a') as file:
        file.write(f'{data}\n')

# InputBox class for user input fields
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.font = get_font(30)  # Use the get_font function to get a font object
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = (0, 0, 0) if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Function to display popup message
def display_popup_message(screen, message):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(message, True, (255, 0, 0))  # Red text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display message for 2 seconds

# Registration page function
def register_page():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Registration")

    font = get_font(36)  # Use the get_font function to get a font object

    background_image = pygame.image.load("registerbackground.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    input_box_width = 400
    input_box_height = 60
    button_width = 150
    button_height = 60
    center_x = SCREEN_WIDTH // 2

    username_box = InputBox(center_x - input_box_width // 2, 200, input_box_width, input_box_height)
    password_box = InputBox(center_x - input_box_width // 2, 320, input_box_width, input_box_height)
    confirm_password_box = InputBox(center_x - input_box_width // 2, 440, input_box_width, input_box_height)
    boxes = [username_box, password_box, confirm_password_box]

    register_button = Button(None, (center_x - button_width, 560), "Register", font, BLACK, GRAY)
    signin_button = Button(None, (center_x + button_width, 560), "Sign In", font, BLACK, GRAY)

    while True:
        screen.blit(background_image, (0, 0))
        for box in boxes:
            box.draw(screen)
        register_button.update(screen)
        signin_button.update(screen)

        screen.blit(font.render("Username:", True, BLACK), (username_box.rect.x, username_box.rect.y - 40))
        screen.blit(font.render("Password:", True, BLACK), (password_box.rect.x, password_box.rect.y - 40))
        screen.blit(font.render("Confirm Password:", True, BLACK), (confirm_password_box.rect.x, confirm_password_box.rect.y - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.check_for_input(pygame.mouse.get_pos()):
                    username = username_box.text
                    password = password_box.text
                    confirm_password = confirm_password_box.text
                    if password == confirm_password:
                        database = read_database(USER_DB_FILE)
                        if username not in database:
                            write_to_database(USER_DB_FILE, f"{username}:{password}")
                            display_popup_message(screen, "Registration successful!")
                            return username
                        else:
                            display_popup_message(screen, "Username already exists!")
                    else:
                        display_popup_message(screen, "Passwords do not match!")
                if signin_button.check_for_input(pygame.mouse.get_pos()):
                    return "SignIn"

if __name__ == "__main__":
    result = register_page()

    if result == "SignIn":
        print("Signing in...")
        try:
            subprocess.run(["python", "Menu.py"], check=True)
        except subprocess.CalledProcessError:
            print("Error launching Menu.py")

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 0, 0) if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def read_database():
    with open('logindatabase.txt', 'r') as file:
        data = file.readlines()
    return {line.split(':')[0]: line.split(':')[1].strip() for line in data}

def write_to_database(username, password):
    with open('logindatabase.txt', 'a') as file:
        file.write(f'{username}:{password}\n')

def draw_message(screen, message):
    msg_surface = font.render(message, True, BLACK)
    screen.blit(msg_surface, (width//2 - msg_surface.get_width()//2, height//2 - 30))

def login_page():
    username_box = InputBox(300, 200, 200, 40)
    password_box = InputBox(300, 300, 200, 40)
    boxes = [username_box, password_box]

    login_button = pygame.Rect(350, 400, 100, 50)
    register_button = pygame.Rect(600, 500, 150, 50)
    message = ""
    login_success_time = None  

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    username = username_box.text
                    password = password_box.text
                    database = read_database()
                    if username in database and database[username] == password:
                        message = "Login successful!"
                        login_success_time = current_time
                    else:
                        message = "Wrong username or password!"
                if register_button.collidepoint(event.pos):
                    return 'register'

        screen.blit(background_image, (0, 0))
        for box in boxes:
            box.draw(screen)
        pygame.draw.rect(screen, GRAY, login_button)
        pygame.draw.rect(screen, GRAY, register_button)
        screen.blit(font.render("Login", True, BLACK), (login_button.x + 15, login_button.y + 10))
        screen.blit(font.render("Register", True, BLACK), (register_button.x + 15, register_button.y + 10))

        screen.blit(font.render("Username:", True, BLACK), (username_box.rect.x - 150, username_box.rect.y + 5))
        screen.blit(font.render("Password:", True, BLACK), (password_box.rect.x - 150, password_box.rect.y + 5))

        draw_message(screen, message)
        
        if login_success_time and current_time - login_success_time > 3000:
            return 'main_menu'
        
        pygame.display.flip()

def register_page():
    username_box = InputBox(300, 200, 200, 40)
    password_box = InputBox(300, 300, 200, 40)
    boxes = [username_box, password_box]

    register_button = pygame.Rect(350, 400, 100, 50)
    back_button = pygame.Rect(600, 500, 150, 50)
    message = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.collidepoint(event.pos):
                    username = username_box.text
                    password = password_box.text
                    database = read_database()
                    if username not in database:
                        write_to_database(username, password)
                        message = "Account registered successfully!"
                    else:
                        message = "Username already exists!"
                if back_button.collidepoint(event.pos):
                    return 'login'

        screen.blit(background_image, (0, 0))
        for box in boxes:
            box.draw(screen)
        pygame.draw.rect(screen, GRAY, register_button)
        pygame.draw.rect(screen, GRAY, back_button)
        screen.blit(font.render("Register", True, BLACK), (register_button.x + 15, register_button.y + 10))
        screen.blit(font.render("Back", True, BLACK), (back_button.x + 15, back_button.y + 10))            

        screen.blit(font.render("Username:", True, BLACK), (username_box.rect.x - 150, username_box.rect.y + 5))
        screen.blit(font.render("Password:", True, BLACK), (password_box.rect.x - 150, password_box.rect.y + 5))

        draw_message(screen, message)
        pygame.display.flip()

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(WHITE)
        screen.blit(font.render("Main Menu", True, BLACK), (width // 2 - 100, height // 2))
        pygame.display.flip()

        # Assuming some condition to return to another page or quit
        # For example, return 'login' to go back to the login page
        return 'login'

# Initialize starting page
current_page = 'login'
while True:
    if current_page == 'login':
        current_page = login_page()
    elif current_page == 'register':
        current_page = register_page()
    elif current_page == 'main_menu':
        current_page = main_menu()
