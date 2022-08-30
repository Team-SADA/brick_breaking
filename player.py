import pygame

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, camera):
        super().__init__()
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill((160, 219, 115))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.9)))
        self.mask = pygame.mask.from_surface(self.image)
        self.max_speed = 30
        self.camera = camera
        self.counter = 0
        self.x = SCREEN_WIDTH // 2

    def update(self):
        if self.counter == 0:
            self.counter = 2
            temp_x = self.camera.get_x()
            self.x = (temp_x / 1080 * 1920) if temp_x != -1 else self.x
        else:
            self.counter -= 1
        dx = self.x - self.rect.centerx
        dx = min(self.max_speed, max(-self.max_speed, dx))
        self.rect.x += dx

        # dx = pygame.mouse.get_pos()[0] - self.rect.centerx
        # dx = min(self.max_speed, max(-self.max_speed, dx))
        # self.rect.x += dx
