import pygame
from engine.colors import HIGHLIGHT, BLACK

class Player:
    def __init__(self, x, y, width=40, height=40, color=HIGHLIGHT, speed=5):
        """ change to cooler person """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # border for visibility
