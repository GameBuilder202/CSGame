import pygame
import pygame.freetype
from pygame.locals import *
from pygame.sprite import Group

from entities import Asteroid, Player, Demon

WIDTH = 1024
HEIGHT = 575

ADD_ASTEROID = pygame.USEREVENT + 1
INC_SCORE = pygame.USEREVENT + 2


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('game')
    clock = pygame.time.Clock()

    pygame.time.set_timer(ADD_ASTEROID, 1000)
    pygame.time.set_timer(INC_SCORE, 1500)

    GAMEOVER_FONT = pygame.freetype.SysFont(None, 80)
    end_text_alpha = 0.0
    SCORE_FONT = pygame.freetype.SysFont(None, 24)

    player = Player(WIDTH, HEIGHT)
    demon = Demon(WIDTH, HEIGHT)
    grp = Group(player, demon)

    score = 0

    asteroids: Group[Asteroid] = Group()

    pressed: tuple[int, ...] = tuple[int]()

    running = True
    game_running = running
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == ADD_ASTEROID and game_running:
                asteroids.add(Asteroid(WIDTH, HEIGHT))
            if event.type == INC_SCORE and game_running:
                score += 1

        if game_running:
            screen.fill((10, 0, 0))

            last_pressed = pressed
            pressed = pygame.key.get_pressed()
            player.update(pressed, last_pressed)

            asteroid: Asteroid
            for asteroid in asteroids:
                asteroid.update()

            if pygame.sprite.spritecollideany(player, asteroids) \
                    or pygame.sprite.spritecollide(player, [demon], False):
                game_running = False

            for asteroid in asteroids:
                asteroid.blit(screen)
            entity: Player | Demon
            for entity in grp:  # type: ignore
                entity.blit(screen)
        else:
            GAMEOVER_FONT.render_to(
                screen,
                (WIDTH // 4, HEIGHT // 2 - 40),
                "GAME OVER",
                (255, 50, 50, (end_text_alpha * 255).__floor__())
            )
            SCORE_FONT.render_to(
                screen,
                (WIDTH // 2 - 100, HEIGHT // 2 + 40),
                f"FINAL SCORE: {score}",
                (255, 50, 50, (end_text_alpha * 255).__floor__())
            )
            end_text_alpha = clamp(end_text_alpha + 0.02, 0, 1)

        SCORE_FONT.render_to(
            screen,
            (10, 10),
            str(score),
            (200, 200, 50)
        )

        clock.tick(60)
        pygame.display.update()

    pygame.quit()


def clamp(val: float, minv: float, maxv: float) -> float:
    return min(max(val, minv), maxv)


if __name__ == '__main__':
    main()
