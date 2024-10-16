import pygame
from pygame.math import Vector2
from pygame import Surface
from pygame.locals import *

import random


def clamp(val: int | float, minv: int | float, maxv: int | float) -> int | float:
    return min(max(val, minv), maxv)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int) -> None:
        super().__init__()
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        self.image = pygame.image.load('assets/player.png')
        self.dims = (15, 15)
        self.image = pygame.transform.scale(self.image, self.dims)
        self.rect = self.image.get_rect()

        self.vel = Vector2(0.0, 0.0)
        self.SPEED = 0.10
        self.JUMP = 3
        self.GRAVITY = 0.5
        self.FLOATINESS_X = 0.98
        self.FLOATINESS_Y = 0.94

        self.rect.move_ip(
            (screen_width - self.dims[0]) / 2,
            (screen_height - self.dims[1]) / 2,
        )

    def blit(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self, keys: tuple[int, ...], last_keys: tuple[int, ...]) -> None:
        super().update()

        if keys[K_LEFT]:
            self.vel.x += -self.SPEED
        if keys[K_RIGHT]:
            self.vel.x += self.SPEED

        self.vel.y += self.GRAVITY

        if keys[K_SPACE] and not last_keys[K_SPACE]:
            self.vel.y = -self.JUMP

        self.vel = Vector2(self.vel.x * self.FLOATINESS_X, self.vel.y * self.FLOATINESS_Y)
        self.rect.move_ip(self.vel.x, self.vel.y)

        self.rect.x = clamp(self.rect.x, 0, self.SCREEN_WIDTH - self.dims[0])
        self.rect.y = clamp(self.rect.y, 0, self.SCREEN_HEIGHT - self.dims[1])


# When we say demon we actually mean monster
class Demon(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int) -> None:
        super().__init__()
        self.image = pygame.image.load('assets/demon.png')
        self.image = pygame.transform.scale_by(
            self.image,
            screen_width / self.image.get_width()
        )
        self.rect = self.image.get_rect()

        self.rect.move_ip(0, screen_height - self.rect.height)

    def blit(self, screen: Surface):
        screen.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int) -> None:
        super().__init__()
        self.image = pygame.image.load('assets/asteroid.png')
        self.rect = self.image.get_rect()
        self.screen_height = screen_height

        self.rect.move_ip(random.randint(0, screen_width), 0)

    def blit(self, screen: Surface):
        screen.blit(self.image, self.rect)

    def update(self) -> None:
        super().update()

        self.rect.move_ip(0, 2)

        if self.rect.y >= self.screen_height - self.rect.height:
            self.kill()
