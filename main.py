# Example file showing a circle moving on screen
import pygame
from settings import WIDTH, HEIGHT, bar_width, bar_height, block_width, block_height, score_popups

from blocks import draw_blocks, draw_points

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(WIDTH // 2, HEIGHT - 300)

ball = pygame.draw.circle(screen, "red", player_pos, 20)
bar = pygame.Rect((WIDTH - bar_width) // 2, HEIGHT - 130, bar_width, bar_height)
# speed = [X direction speed, Y direction speed]
speed = [4, 4]

blocks = []
deleted_blocks = []
waiting = True
bounce_zero = True

pygame.font.init()
my_font = pygame.font.SysFont("Comic Sans MS", 20)
points_font = pygame.font.SysFont("Comic Sans MS", 30, True)

title = pygame.image.load("images/pygame_logo.png").convert_alpha()
title_scaling = pygame.transform.scale(title, (WIDTH - 10, 100))
title_height = title_scaling.get_height()
title_width = title_scaling.get_width()

looser = pygame.image.load("images/looser.png").convert_alpha()
looser_scaling = pygame.transform.scale(looser, (WIDTH // 2, 300))
looser_height = looser_scaling.get_height()
looser_width = looser_scaling.get_width()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    blocks = draw_blocks(screen, deleted_blocks)

    # game title
    screen.blit(title_scaling, ((WIDTH - title_width) // 2, 20))

    # points counter
    points = 0

    while bounce_zero:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bounce_zero = False
                running = False
        screen.fill("purple")
        screen.blit(title_scaling, ((WIDTH - title_width) // 2, 20))
        ball = ball.move([0, 1])
        pygame.draw.circle(screen, "red", ball.center, 20)
        pygame.draw.rect(screen, "black", bar)
        draw_blocks(screen, deleted_blocks)
        pygame.display.flip()
        clock.tick(60)
        if ball.colliderect(bar):
            bounce_zero = False

    keys = pygame.key.get_pressed()

    current_x = player_pos[0]
    current_y = player_pos[1]

    if ball.left <= 0 or ball.right >= WIDTH:
        speed[0] = -speed[0]
    if ball.top <= 0:
        speed[1] = -speed[1]
    if ball.colliderect(bar):
        speed[1] = -speed[1]
        # avoiding ball slicing through the bar
        if speed[1] < 0:
            ball.bottom = bar.top
        else:
            ball.top = bar.bottom
    if ball.bottom >= HEIGHT:
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                waiting = False
                running = False
            if keys[pygame.K_a]:
                waiting = False
                ball = pygame.draw.circle(
                    screen, "red", player_pos, 20
                ) 
                bounce_zero = True
                speed = [4, 4]
                deleted_blocks = []
                bar.topleft = ((WIDTH - bar_width) // 2, HEIGHT - 130)
                # ball.move([0, 1])
            screen.fill("black")
            screen.blit(
                looser_scaling,
                ((WIDTH - looser_width) // 2, (HEIGHT - looser_height) // 2),
            )
            text_surface = my_font.render(
                "Press A for a new game.\nPress RETURN to quit the game.",
                False,
                "white",
            )
            width_my_font, height_my_font = my_font.size("Press RETURN to quit the game.")
            screen.blit(
                text_surface,
                ((WIDTH - width_my_font) // 2, 800),
            )
            pygame.display.flip()
            clock.tick(60)
        waiting = True
        continue

    ball = ball.move(speed)

    if keys[pygame.K_LEFT] and bar.left > 0:
        bar.left -= 5
        bar.move([bar.left, 0])
    if keys[pygame.K_RIGHT] and bar.right < WIDTH:
        bar.left += 5
        bar.move([bar.left, 0])

    pygame.draw.circle(screen, "red", ball.center, 20)

    pygame.draw.rect(screen, "black", bar)

    for block, color in blocks:
        if ball.colliderect(block):
            speed[1] = -speed[1]
            print(f"Block hitted: {block.left}, {block.top}")
            if color == (0, 0, 255):
                deleted_blocks.append((block.left, block.top))
                points += 1
                if block.left + block_width < WIDTH and (block.left + block_width, block.top) not in deleted_blocks:
                    deleted_blocks.append((block.left + block_width, block.top))
                    points += 1
                if block.left != 5 and (block.left - block_width, block.top) not in deleted_blocks:
                    deleted_blocks.append((block.left - block_width, block.top))
                    points += 1
                if block.top != 150 and (block.left, block.top - block_height) not in deleted_blocks:
                    deleted_blocks.append((block.left, block.top - block_height))
                    points += 1
                score_popups.append({"pos": [block.centerx, block.centery], "value": points, "timer": 90})
                points = 0
            else:
                deleted_blocks.append((block.left, block.top))
                points += 1
                score_popups.append({"pos": [block.centerx, block.centery], "value": points, "timer": 90})
                points = 0
            break
    draw_points(screen, score_popups, points_font)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
