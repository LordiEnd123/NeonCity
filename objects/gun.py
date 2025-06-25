import pygame
import os


class Bullet:
    def __init__(self, x, y, direction, speed=8):
        self.direction = direction
        self.speed = speed
        self.active = True

        base_image = pygame.image.load(os.path.join("img", "bullet.png")).convert_alpha()
        base_image = pygame.transform.scale(base_image, (30, 15))

        if direction == "right":
            self.image = base_image
        elif direction == "left":
            self.image = pygame.transform.rotate(base_image, 180)
        elif direction == "up":
            self.image = pygame.transform.rotate(base_image, 90)
        elif direction == "down":
            self.image = pygame.transform.rotate(base_image, -90)

        self.rect = self.image.get_rect(center=(x, y))

    def update(self, obstacles):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # Границы экрана
        if (self.rect.right < 0 or self.rect.left > 1300 or
                self.rect.bottom < 0 or self.rect.top > 700):
            self.active = False

        # Проверка на столкновения
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                self.active = False
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
       # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_collision(self, hitbox):
        return self.active and self.rect.colliderect(hitbox)


class Gun:
    def __init__(self, x, y, direction="left", fire_rate=60, sound_manager=None):
        self.base_image = pygame.image.load(os.path.join("img", "gun.png")).convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (50, 50))

        self.direction = direction
        self.image = self.rotate_img(self.base_image, direction)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.fire_rate = fire_rate
        self.timer = 0
        self.bullets = []
        self.sound_manager = sound_manager

    def rotate_img(self, image, direction):
        if direction == "right":
            return image
        elif direction == "left":
            return pygame.transform.rotate(image, 180)
        elif direction == "up":
            return pygame.transform.rotate(image, 90)
        elif direction == "down":
            return pygame.transform.rotate(image, -90)

    def update(self, obstacles):
        self.timer += 0.8
        if self.timer >= self.fire_rate:
            self.timer = 0

            if self.direction == "right":
                bullet_x = self.rect.right
                bullet_y = self.rect.centery
            elif self.direction == "left":
                bullet_x = self.rect.left
                bullet_y = self.rect.centery
            elif self.direction == "up":
                bullet_x = self.rect.centerx
                bullet_y = self.rect.top
            elif self.direction == "down":
                bullet_x = self.rect.centerx
                bullet_y = self.rect.bottom

            self.bullets.append(Bullet(bullet_x, bullet_y, self.direction))
            if self.sound_manager:
                self.sound_manager.play_effect("gun")

        for bullet in self.bullets:
            bullet.update(obstacles)

        self.bullets = [b for b in self.bullets if b.active]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_bullet_hits(self, player_hitbox):
        for bullet in self.bullets:
            if bullet.check_collision(player_hitbox):
                bullet.active = False
                return True
        return False