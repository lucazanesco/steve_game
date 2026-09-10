import pygame
from settings import WIDTH, HEIGHT, block_width, block_height, score_popups, GRID_START_X, GRID_START_Y



def draw_points(screen, score_popups, font):
    for popup in score_popups:
        text_surface = font.render(
            f"+{popup['value']}",
            True,
            "green",
        )
        screen.blit(
            text_surface,
            (popup["pos"]),
        )
        popup["pos"][1] -= 1
        popup["timer"] -= 1
        if popup["timer"] <= 0:
            score_popups.remove(popup)


def draw_blocks(screen, deleted_blocks):
    blocks = []
    x = GRID_START_X
    y = GRID_START_Y
    number = 0
    while x < WIDTH - 5 and y < HEIGHT // 2:
        number += 1
        if (x, y) not in deleted_blocks:
            rect = pygame.Rect(x, y, block_width - 10, block_height - 5)
            if (y + number) % 3 == 0:
                color = (0, 0, 255)
                pygame.draw.rect(screen, color, rect)
            else:
                color = (255, 255, 0)
                pygame.draw.rect(screen, color, rect)
            print(f"Block created:  {rect.x} {rect.y}")
            blocks.append((rect, color))
        x += block_width
        if x >= WIDTH:
            x = GRID_START_X
            y += block_height
    return blocks

def end_or_restart(screen, font, image, image_pos, clock):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return False, True
        if keys[pygame.K_a]:
            return True, False 
        screen.fill("black")
        screen.blit(image, image_pos)
        text_surface = font.render(
            "Press A for a new game.\nPress RETURN to quit the game.",
            False,
            "white",
        )
        width_my_font, height_my_font = font.size("Press RETURN to quit the game.")
        screen.blit(
            text_surface,
            ((WIDTH - width_my_font) // 2, 800),
        )
        pygame.display.flip()
        clock.tick(60)
    
