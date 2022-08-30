import math
import pygame

from settings import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, brick_group, player_group):
        super().__init__()
        self.image = pygame.Surface(BALL_SIZE).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (160, 219, 115), (BALL_RADIUS,) * 2, BALL_RADIUS)
        self.rect = self.image.get_rect(center=pos)
        self.speed = pygame.math.Vector2(1, 1)
        self.brick_group = brick_group
        self.player_group = player_group
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 9
        self.vector = pygame.math.Vector2(0, 10)
        self.pos = pygame.math.Vector2(*pos)

    def brick_collide(self):
        for brick in self.brick_group.sprites():
            offset = brick.rect.x - self.rect.x, brick.rect.y - self.rect.y
            if self.mask.overlap_area(brick.mask, offset) <= 0:
                continue

            if brick.rect.bottom >= self.rect.centery >= brick.rect.top or \
                    self.vector.y > 0 and self.rect.centery > brick.rect.bottom or \
                    self.vector.y < 0 and self.rect.centery < brick.rect.top:
                self.vector.x *= -1
            elif brick.rect.left <= self.rect.centerx <= brick.rect.right or \
                    self.vector.x > 0 and self.rect.centerx > brick.rect.right or \
                    self.vector.x < 0 and self.rect.centerx < brick.rect.left:
                self.vector.y *= -1
            else:
                self.vector *= -1
            brick.kill()
            self.speed += 0.15

    def player_collide(self):
        player = self.player_group.sprite
        offset = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        if self.mask.overlap_area(player.mask, offset) > 0:
            if player.rect.collidepoint(self.rect.center) or self.rect.centery > player.rect.bottom:
                self.rect.top = player.rect.bottom
                self.vector = pygame.math.Vector2(0, 10)
            elif player.rect.bottom > self.rect.centery > player.rect.top:
                self.vector.x *= -1
            else:
                temp = player.rect.centerx - self.rect.centerx
                temp = abs(temp ** 0.7) * (1 if temp > 0 else -1)
                angle = -90 - temp * 2
                self.vector.x = math.cos(math.radians(angle))
                self.vector.y = math.sin(math.radians(angle))
                self.vector *= self.speed

    def update(self):
        self.pos += self.vector
        self.rect.center = round(self.pos.x), round(self.pos.y)

        if self.rect.left < 0:
            self.vector.x = abs(self.vector.x)
        if self.rect.right > SCREEN_WIDTH:
            self.vector.x = -abs(self.vector.x)
        if self.rect.top < 0:
            self.vector.y *= -1
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        self.brick_collide()
        self.player_collide()
