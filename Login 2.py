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

current_page = 'login'
while True:
    if current_page == 'login':
        current_page = login_page()
    elif current_page == 'register':
        current_page = register_page()
    elif current_page == 'main_menu':
        main_menu()