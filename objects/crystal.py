import pygame
import math


class Crystal:
    def __init__(self, x, y, image, tile_size):
        self.original_image = pygame.transform.scale(image, (tile_size, tile_size))
        self.image = self.original_image
        self.base_x = x + tile_size // 2
        self.base_y = y + tile_size // 2
        self.rect = self.image.get_rect(center=(self.base_x, self.base_y))
        self.collected = False
        self.float_amplitude = 4
        self.float_frequency = 1
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        if not self.collected:
            ticks = pygame.time.get_ticks() - self.start_ticks
            time_sec = ticks / 1000
            float_offset = math.sin(time_sec * self.float_frequency * math.pi * 2) * self.float_amplitude
            self.rect.center = (self.base_x, self.base_y + float_offset)

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True
        return False