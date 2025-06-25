import pygame


class Deadly:
    def __init__(self, x, y, image, tile_size):
        self.image = pygame.transform.scale(image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
      # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_collision(self, player_hitbox):
        return self.rect.colliderect(player_hitbox)