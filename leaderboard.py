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

    def format_time(self, seconds):
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes:02d} minutes {seconds:02d} seconds"

    def display_leaderboard(self):
        font = pygame.font.Font(None, 24)  # Decreased font size
        y_offset = 50
        line_height = 30
        column_width = 200

        self.screen.fill(WHITE)   

        header = font.render("Player", True, BLACK)
        self.screen.blit(header, (50, 20))
        for i, level in enumerate(["Level 1", "Level 2", "Level 3"], start=1):
            header = font.render(level, True, BLACK)
            self.screen.blit(header, (50 + i * column_width, 20))

        for player, times in self.leaderboard.player_times.items():
            player_label = font.render(player, True, BLACK)
            self.screen.blit(player_label, (50, y_offset))

            for i, level in enumerate(["level1", "level2", "level3"], start=1):
                time_text = self.format_time(times[level])
                time_label = font.render(time_text, True, BLACK)
                self.screen.blit(time_label, (50 + i * column_width, y_offset))

            y_offset += line_height

            for i in range(len(self.leaderboard.player_times) + 1):
            pygame.draw.line(self.screen, GRAY, (50, 20 + i * line_height), (50 + 4 * column_width, 20 + i * line_height), 1)
            for i in range(5):
            pygame.draw.line(self.screen, GRAY, (50 + i * column_width, 20), (50 + i * column_width, 20 + (len(self.leaderboard.player_times) + 1) * line_height), 1)

            pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.display_leaderboard()
            pygame.display.update()

        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()