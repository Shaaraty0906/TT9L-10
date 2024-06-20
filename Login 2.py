import pygame
import sys

pygame.init() 

# setting for screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Login and Registration System")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 36)

background_image = pygame.image.load("loginbackground2.jpg")
background_image = pygame.transform.scale(background_image, (width, height))