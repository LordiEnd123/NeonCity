import pygame
import os


class Enemy:
    def __init__(self, x, y, move_range=100, speed=2):
        self.walk_images = []
        for i in range(1, 3):
            img = pygame.image.load(os.path.join("img", f"enemy_{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (80, 80))
            self.walk_images.append(img)

        self.image_index = 0
        self.animation_counter = 0
        self.image = self.walk_images[0]

        self.rect = self.image.get_rect(topleft=(x, y))

        # Хитбокс
        self.hitbox_offset_left = 22
        self.hitbox_offset_right = 22
        self.hitbox_offset_top = 25
        self.hitbox_offset_bottom = 1

        self.update_hitbox()

        # Движение
        self.start_x = x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1
        self.dy = 0
        self.vel_y = 0
        self.in_air = True

    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.rect.x + self.hitbox_offset_left, self.rect.y + self.hitbox_offset_top,
                                  self.rect.width - self.hitbox_offset_left - self.hitbox_offset_right,
                                  self.rect.height - self.hitbox_offset_top - self.hitbox_offset_bottom)

    def apply_physics(self):
        self.vel_y += 1
        self.vel_y = min(self.vel_y, 10)
        self.dy = self.vel_y

    def move(self, world):
        self.in_air = True
        next_x = self.rect.centerx + self.direction * self.speed
        foot_y = self.rect.bottom + 1

        tile_below = pygame.Rect(next_x, foot_y, 1, 1)
        has_ground = any(tile[1].colliderect(tile_below) for tile in world.tile_list)

        if not has_ground:
            self.direction *= -1
            return

        # Горизонтальное движение
        self.rect.x += self.speed * self.direction
        self.update_hitbox()

        for tile in world.tile_list:
            if tile[1].colliderect(self.hitbox):
                self.direction *= -1
                self.rect.x += self.speed * self.direction
                self.update_hitbox()
                break

        # Вертикальное движение
        self.rect.y += self.dy
        self.update_hitbox()
        for tile in world.tile_list:
            if tile[1].colliderect(self.hitbox):
                if self.vel_y > 0:
                    self.rect.y = tile[1].top - self.hitbox.height - self.hitbox_offset_top
                    self.vel_y = 0
                    self.in_air = False
                    self.update_hitbox()
                break

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.image_index = (self.image_index + 1) % len(self.walk_images)
        self.image = self.walk_images[self.image_index]

    def update(self, world):
        self.apply_physics()
        self.move(world)
        self.update_animation()

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
        screen.blit(flipped_image, self.rect)
       # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def check_collision(self, player_rect):
        return self.hitbox.colliderect(player_rect)
