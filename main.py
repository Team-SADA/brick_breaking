import itertools
import json
import time
import pygame
import os
import sys

from ball import Ball
from brick import Brick
from player import Player
from camera import Camera
from settings import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
camera = Camera()


if not os.path.exists("highscore.json"):
    with open("highscore.json", "w") as f:
        json.dump({}, f)


def draw_text(text, *, center=None, size=None, color=None):
    font = pygame.font.Font("D2Coding.ttf", size or 24)
    text = font.render(text, True, color or (255, 255, 255))
    if center is None:
        text_rect = text.get_rect()
        text_rect.centerx = SCREEN_WIDTH // 2
        text_rect.centery = SCREEN_HEIGHT // 2
    else:
        text_rect = text.get_rect(center=center)
    screen.blit(text, text_rect)


def end(*_):
    camera.delete()
    pygame.quit()
    sys.exit()


def main(*_):
    time_count = 180
    player = Player(camera)
    player_group = pygame.sprite.GroupSingle(player)
    brick_group = pygame.sprite.Group()
    color_map = (255, 162, 170), (255, 177, 156), (255, 192, 132), (255, 208, 98)

    for i, j in itertools.product(range(8), range(4)):
        x = SCREEN_WIDTH / 16 * (2 * i + 1)
        y = SCREEN_HEIGHT / 8 * (j + 1.4)
        Brick((x, y), brick_group, color_map[j])
    ball = Ball((960, 750), brick_group, player_group)
    ball_group = pygame.sprite.GroupSingle(ball)
    start_time = time.perf_counter()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return end,

        screen.fill((255, 238, 229))
        time_count -= 1
        if time_count == 0:
            start_time = time.perf_counter()
        if time_count <= 0:
            ball_group.update()
            if len(ball_group.sprites()) == 0:
                return game_over, len(brick_group.sprites())
            if len(brick_group.sprites()) == 0:
                return clear, time.perf_counter() - start_time
            time_text = f"{time.perf_counter() - start_time:.2f}"
            draw_text(time_text, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 21), size=52)
        player_group.update()
        # hanbyeol = pygame.image.load("img.png").convert_alpha()
        # hanbyeol_rect = hanbyeol.get_rect(midtop=player.rect.midbottom)
        # screen.blit(hanbyeol, hanbyeol_rect)
        ball_group.draw(screen)
        brick_group.draw(screen)
        player_group.draw(screen)

        if time_count > 0:
            draw_text(f"{time_count // 60 + 1}", size=480, color=(55, 55, 55))

        pygame.display.update()
        clock.tick(FPS)


def game_over(remaining, *_):
    time_count = 180
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return end,

        time_count -= 1
        if time_count <= 0:
            return leaderboard,

        screen.fill((0, 0, 0))
        draw_text("GAME OVER!", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), size=96)
        draw_text(f"{remaining} bricks were remaining", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 * 2), size=54)
        pygame.display.update()
        clock.tick(FPS)


def clear(clear_time, *_):
    time_count = 180
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return end,

        time_count -= 1
        if time_count <= 0:
            return record, clear_time

        screen.fill((0, 0, 0))
        draw_text("CLEAR!", size=96)
        draw_text(f"clear time: {clear_time:.4f}", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 * 2), size=54)
        pygame.display.update()
        clock.tick(FPS)


def record(clear_time, *_):
    string = ""
    backspace_count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return end,
            if event.key == pygame.K_BACKSPACE:
                backspace_count = 25
                string = string[:-1]
            elif event.key == pygame.K_RETURN and string:
                with open("highscore.json", "r") as g:
                    data = json.load(g)
                data[string] = clear_time
                with open("highscore.json", "w") as g:
                    json.dump(data, g)
                return leaderboard,
            else:
                string += event.unicode
                string = string[:20]
        if backspace_count > 0:
            backspace_count -= 1
        else:
            backspace_count = 2
            string = string[:-1]

        if not pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            backspace_count = 100

        screen.fill((0, 0, 0))
        draw_text("Enter Your Name", size=96, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 11 * 4))
        draw_text(string, size=64, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 7 * 4))
        pygame.display.update()
        clock.tick(FPS)


def leaderboard(*_):
    with open("highscore.json", "r") as g:
        data = json.load(g)
    data = list(data.items())
    data.sort(key=lambda x: x[1])
    data = data[:10]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return end,
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return main,
        screen.fill((0, 0, 0))
        draw_text("LEADERBOARD", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 12), size=96)
        for i, line in enumerate(data):
            y = SCREEN_HEIGHT // 16 * (i + 4)
            draw_text(f"{i + 1}. Name: {line[0]}, Time: {line[1]:.4f}", center=(SCREEN_WIDTH // 2, y), size=48)
        draw_text("press ENTER to replay", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 12 * 11), size=36)
        pygame.display.update()
        clock.tick(FPS)


func = main
params = ()
while __name__ == "__main__":
    result = func(*params)
    func, *params = result
