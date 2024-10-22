import pygame
import sys
import settings
from level import Level
from importer import json_dump

font = pygame.font.Font(None, 100)


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption('Naturalist')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings.IS_TASKED = False
                    self.level.save["level"] = 0
                    json_dump(settings.SAVE_PATH, self.level.save)
                    pygame.quit()
                    sys.exit()

            if self.level.save["last_level"] == 4:
                self.screen.fill('black')
                text = font.render("Congrats! You beat the game!", True, 'White')
                self.screen.blit(text, (0, 0))
                pygame.display.update()
                self.clock.tick(settings.FPS)
                continue

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(settings.FPS)


if __name__ == '__main__':
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
