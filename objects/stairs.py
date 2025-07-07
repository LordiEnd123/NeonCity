import pygame
import os


class Stair:
    def __init__(self, x, y, tile_size, is_top=False):
        self.image = pygame.image.load(os.path.join("img", "st.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.is_top = is_top

        if self.is_top:
            self.rect = pygame.Rect(x, y - 1, tile_size, tile_size + 10)
        else:
            self.rect = pygame.Rect(x, y, tile_size, tile_size)
        self.draw_rect = pygame.Rect(x, y, tile_size, tile_size)

    def draw(self, screen):
        screen.blit(self.image, self.draw_rect)
      #  pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_player_inside(self, player_rect):
        return self.rect.colliderect(player_rect)

    def player_on_top(self, player_hitbox):
        return (self.is_top and abs(player_hitbox.bottom - self.rect.top) <= 1 and
                self.rect.left <= player_hitbox.centerx <= self.rect.right)