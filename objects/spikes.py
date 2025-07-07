import pygame
import os


class Spike:
    def __init__(self, x, y, tile_size, sound_manager, active_duration=60, inactive_duration=60):
        self.tile_size = tile_size
        self.x = x
        self.y = y
        self.sound_manager = sound_manager
        self.active_duration = active_duration
        self.inactive_duration = inactive_duration
        self.timer = 0
        self.active = False

        self.image_up = pygame.image.load(os.path.join("img", "sp_2.png")).convert_alpha()
        self.image_down = pygame.image.load(os.path.join("img", "sp_1.png")).convert_alpha()
        self.image_up = pygame.transform.scale(self.image_up, (tile_size, tile_size))
        self.image_down = pygame.transform.scale(self.image_down, (tile_size, tile_size))

        self.rect = pygame.Rect(x, y, tile_size, tile_size)

    def update(self):
        self.timer += 1
        if self.active and self.timer >= self.active_duration:
            self.active = False
            self.timer = 0
            self.sound_manager.play_effect("spikes")
        elif not self.active and self.timer >= self.inactive_duration:
            self.active = True
            self.timer = 0
            self.sound_manager.play_effect("spikes")

    def draw(self, screen):
        image = self.image_up if self.active else self.image_down
        screen.blit(image, (self.x, self.y))
       # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_collision(self, player_hitbox):
        return self.active and self.rect.colliderect(player_hitbox)