import pygame
import time
import json

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Leaderboard:
    def __init__(self):
        self.player_times = {
            "player1": {"level1": 30, "level2": 45, "level3": 60},
            "player2": {"level1": 40, "level2": 50, "level3": 70},
            "player3": {"level1": 35, "level2": 55, "level3": 65},