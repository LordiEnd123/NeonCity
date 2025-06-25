import pygame
from objects.kill_block import Deadly


class RotatingDeadly(Deadly):
    def __init__(self, x, y, image, tile_size, rotation_speed=5, hitbox_shrink=(20, 20), scale=1.8):
        super().__init__(x, y, image, tile_size)
        self.rotation_speed = rotation_speed
        self.angle = 0

        scaled_size = int(tile_size * scale)
        self.original_image = pygame.transform.scale(image, (scaled_size, scaled_size))
        self.image = self.original_image
        self.rect = self.original_image.get_rect(center=(x + tile_size // 2, y + tile_size // 2))

        self.hitbox = self.rect.inflate(-hitbox_shrink[0], -hitbox_shrink[1])

    def update(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def draw(self, screen):
        rotated_rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, rotated_rect)
       # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def check_collision(self, player_hitbox):
        return self.hitbox.colliderect(player_hitbox)