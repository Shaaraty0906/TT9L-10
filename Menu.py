import pygame
import sys
import os
import subprocess

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu page")


# Function to load font
def get_font(size):
    return pygame.font.Font("assets/arial.ttf", size)

# Class for buttons
class Button():
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

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('lightskyblue3')
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on click inside input box
            self.active = self.rect.collidepoint(event.pos)
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Update the text surface
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class PopupMessage:
    def __init__(self, text, font, color, duration=3000):
        self.text = text
        self.font = font
        self.color = color
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.visible = False

    def show(self, text):
        self.text = text
        self.visible = True
        self.start_time = pygame.time.get_ticks()

    def update(self, screen):
        if self.visible:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.visible = False
            else:
                text_render = self.font.render(self.text, True, self.color)
                text_rect = text_render.get_rect(topright=(SCREEN_WIDTH - 20, 20))
                screen.blit(text_render, text_rect)

def level_selection():
    while True:
        SCREEN.fill("black")

        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        LEVEL_TEXT = get_font(50).render("Select a Level", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        LEVEL_1_BUTTON = Button(image=None, pos=(640, 250),
                                text_input="Level 1", font=get_font(50), base_color="White", hovering_color="Green")
        LEVEL_2_BUTTON = Button(image=None, pos=(640, 350),
                                text_input="Level 2", font=get_font(50), base_color="White", hovering_color="Green")
        LEVEL_3_BUTTON = Button(image=None, pos=(640, 450),
                                text_input="Level 3", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        RESULTS_BUTTON = Button(image=None, pos=(640, 500),
                                text_input="Results", font=get_font(50), base_color="White", hovering_color="Green")

        for button in [LEVEL_1_BUTTON, LEVEL_2_BUTTON, LEVEL_3_BUTTON, BACK_BUTTON, RESULTS_BUTTON]:
            button.changeColor(LEVEL_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    subprocess.Popen(["python", "easy.py"])  # Launch easy.py
                elif LEVEL_2_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    subprocess.Popen(["python", "medium.py"])  # Launch medium.py
                elif LEVEL_3_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    subprocess.Popen(["python", "hardlevel.py"])  # Launch hard.py
                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    return  # Return to main_menu
                elif RESULTS_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    subprocess.Popen(["python", "results.py"])

        pygame.display.update()

def INSTRUCTION():
    instructions = [
        "LEVEL 1 - You have to select the tile for slide and use arrow button movement",
        "LEVEL 2 - You have to select the tile for slide and use arrow button for movement.",
        "After you finish this level you will have to guess the picture of the puzzle where",
        "you have to type your answer in a space given.",
        "LEVEL 3 - You have to drag and drop the tile in a free space to complete your puzzle."
    ]
    
    while True:
        INSTRUCTION_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        y_offset = 150
        for line in instructions:
            INSTRUCTION_TEXT = get_font(30).render(line, True, "Black")
            INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, y_offset))
            SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
            y_offset += 40

        INSTRUCTION_BACK = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

        INSTRUCTION_BACK.changeColor(INSTRUCTION_MOUSE_POS)
        INSTRUCTION_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTION_BACK.checkForInput(INSTRUCTION_MOUSE_POS):
                    return  # Return to main_menu

        pygame.display.update()

def main_menu(username):
    background_image = pygame.image.load('mainbackground2.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_large = get_font(36)
    font_small = get_font(24)  # Define a smaller font size

    while True:
        SCREEN.blit(background_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="Play", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        INSTRUCTION_BUTTON = Button(image=None, pos=(640, 400), 
                            text_input="Instruction", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550), 
                            text_input="Quit", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        # Display greeting message with username in the corner
        greeting_text = font_small.render(f"Hi {username}!", True, (255, 255, 255))
        greeting_rect = greeting_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        SCREEN.blit(greeting_text, greeting_rect)

        for button in [PLAY_BUTTON, INSTRUCTION_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    level_selection()  # Go to level selection screen
                elif INSTRUCTION_BUTTON.checkForInput(MENU_MOUSE_POS):
                    INSTRUCTION()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def read_database(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        data = file.readlines()
    return {line.split(':')[0]: line.split(':')[1].strip() for line in data}

def write_to_database(file_path, data):
    with open(file_path, 'a') as file:
        file.write(f'{data}\n')

def login_page():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Login")

    font = get_font(36)

    background_image = pygame.image.load("loginbackground2.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    input_box_width = 400
    input_box_height = 60
    button_width = 150
    button_height = 60
    center_x = SCREEN_WIDTH // 2

    username_box = InputBox(center_x - input_box_width // 2, 220, input_box_width, input_box_height)
    password_box = InputBox(center_x - input_box_width // 2, 340, input_box_width, input_box_height)

    boxes = [username_box, password_box]

    # Center the login button horizontally
    login_button = Button(None, (center_x - button_width // 10, 460), "Login", font, (0, 0, 0), (200, 200, 200))

    # Popup message setup
    popup_message = PopupMessage("", get_font(24), pygame.Color('red'))
    success_message = PopupMessage("", get_font(24), pygame.Color('green'))

    while True:
        screen.blit(background_image, (0, 0))
        for box in boxes:
            box.draw(screen)
        login_button.update(screen)

        screen.blit(font.render("Username:", True, (0, 0, 0)), (username_box.rect.x, username_box.rect.y - 40))
        screen.blit(font.render("Password:", True, (0, 0, 0)), (password_box.rect.x, password_box.rect.y - 40))

        # Update and draw popup messages
        popup_message.update(screen)
        success_message.update(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.checkForInput(pygame.mouse.get_pos()):
                    username = username_box.text
                    password = password_box.text
                    database = read_database('logindatabase.txt')
                    if username in database and database[username] == password:
                        success_message.show("Login successful!")
                        pygame.time.wait(1500)  # Show success message for 1.5 seconds
                        return username  # Return the logged-in username
                    else:
                        popup_message.show("Invalid username or password")

if __name__ == "__main__":
    logged_in_user = login_page()
    if logged_in_user:
        main_menu(logged_in_user)
