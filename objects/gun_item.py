import pygame
import os
import math


class GunItem:
    def __init__(self, x, y):
        self.original_image = pygame.image.load(os.path.join("img", "gun1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (40, 40))

        self.base_x = x + 25
        self.base_y = y + 20

        self.rect = self.image.get_rect(center=(self.base_x, self.base_y))
        self.collision_rect = self.rect.inflate(-30, -30)

        self.picked_up = False
        self.float_amplitude = 4
        self.float_frequency = 1
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        if not self.picked_up:
            ticks = pygame.time.get_ticks() - self.start_ticks
            time_sec = ticks / 1000
            float_offset = math.sin(time_sec * self.float_frequency * math.pi * 2) * self.float_amplitude
            self.rect.center = (self.base_x, self.base_y + float_offset)
            self.collision_rect.center = self.rect.center

    def draw(self, screen):
        if not self.picked_up:
            screen.blit(self.image, self.rect)
       # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_collision(self, player_rect):
        if not self.picked_up and self.collision_rect.colliderect(player_rect):
            self.picked_up = True
            return True
        return False