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
        }

    def record_time(self, player_name, level):
        start_time = time.time()
        time.sleep(2)  # This would be your game logic
        end_time = time.time()
        time_taken = end_time - start_time
        self.player_times[player_name][level] = time_taken

    def save(self, filename='leaderboard.json'):
        with open(filename, 'w') as f:
            json.dump(self.player_times, f, indent=4)

    def load(self, filename='leaderboard.json'):
        try:
            with open(filename, 'r') as f:
                self.player_times = json.load(f)
        except FileNotFoundError:
            pass

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption('Leaderboard')
        self.leaderboard = Leaderboard()
        self.leaderboard.load()               