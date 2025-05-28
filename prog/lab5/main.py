import pygame
import random
import sys

pygame.init()


class Block:
    def __init__(self, dirs: set[str]):
        self.dirs = dirs.copy()

    def rotate(self):
        mapping = {"up": "right", "right": "down", "down": "left", "left": "up"}
        self.dirs = {mapping[d] for d in self.dirs}


vertical_blocks = Block({"up", "down"})

screen = pygame.display.set_mode((1200, 800))
screen.fill((255, 255, 255))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
