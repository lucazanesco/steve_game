import pygame
from settings import WIDTH, HEIGHT, block_width, block_height


def draw_blocks(screen, deleted_blocks):
    blocks = []
    x = 0
    y = 6 * block_height
    number = 0
    while x < WIDTH - 5 and y < HEIGHT // 2:
        number += 1
        if (x + 5, y) not in deleted_blocks:
            rect = pygame.Rect(x + 5, y, block_width - 10, block_height - 5)
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
            x = 0
            y += block_height
    return blocks
