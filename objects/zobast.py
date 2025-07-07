import pygame
import os


class ToothyEnemy:
    def __init__(self, x, y, tile_size, sound_manager, activation_range=10):
        self.tile_size = tile_size
        self.rect = pygame.Rect(x, y, tile_size, tile_size)
        self.sound_manager = sound_manager
        self.active = False
        self.activation_range = activation_range
        self.image_open = pygame.transform.scale(pygame.image.load(os.path.join("img", "zubastik1.png")), (tile_size, tile_size))
        self.image_closed = pygame.transform.scale(pygame.image.load(os.path.join("img", "zubastik2.png")), (tile_size, tile_size))
        self.image = self.image_open
        self.attack_played = False

    def update(self, player_hitbox):
        overlap = player_hitbox.bottom - self.rect.top
        vertically_landed = 0 <= overlap <= 15
        horizontally_aligned = (player_hitbox.right > self.rect.left and player_hitbox.left < self.rect.right)

        if vertically_landed and horizontally_aligned:
            if not self.active:
                self.sound_manager.play_effect("bite")
            self.active = True
            self.image = self.image_closed
        else:
            self.active = False
            self.image = self.image_open
            self.attack_played = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
      #  pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # для отладки

    def check_collision(self, player_hitbox):
        return self.active and self.rect.colliderect(player_hitbox)
