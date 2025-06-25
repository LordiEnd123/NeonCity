import pygame


class ExitTile:
    def __init__(self, x, y, image, tile_size, rotation_speed=2):
        scale_factor = 1.5
        self.size = int(tile_size * scale_factor)

        self.original_image = pygame.transform.scale(image, (self.size, self.size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
        self.rotation_speed = rotation_speed
        self.angle = 0
        a = 20
        self.hitbox = pygame.Rect(0, 0, self.size - 2 * a, self.size - 2 * a)
        self.hitbox.center = self.rect.center

    def update(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.hitbox.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
       # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def check_collision(self, player_rect):
        return self.hitbox.colliderect(player_rect)