import pygame
import os


class MovingBlock:
    def __init__(self, x, y, width, height,
                 direction='horizontal', move_range=100, speed=2, image_name="moving_block.png"):
        self.image = pygame.image.load(os.path.join("img", image_name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.start_y = y

        self.direction = direction
        self.move_range = move_range
        self.speed = speed
        self.move_dir = 1

    def update(self, player):
        prev_rect = self.rect.copy()

        # Движение платформы
        if self.direction == 'horizontal':
            self.rect.x += self.speed * self.move_dir
            if abs(self.rect.x - self.start_x) >= self.move_range:
                self.move_dir *= -1
        else:
            self.rect.y += self.speed * self.move_dir
            if abs(self.rect.y - self.start_y) >= self.move_range:
                self.move_dir *= -1

        movement = (self.rect.x - prev_rect.x, self.rect.y - prev_rect.y)

        if (player.hitbox.bottom == self.rect.top and player.hitbox.right > self.rect.left and
                player.hitbox.left < self.rect.right and player.vel_y >= 0):
            future_rect = player.hitbox.move(movement[0], 0)
            blocked = any(tile[1].colliderect(future_rect) for tile in player.world.tile_list)
            if not blocked:
                player.rect.x += movement[0]
            else:
                player.in_air = True
                player.vel_y = 1

            player.rect.y += movement[1]
            player.update_hitbox()

        elif self.rect.colliderect(player.hitbox):
            future_rect = player.hitbox.move(movement[0], 0)
            blocked = any(tile[1].colliderect(future_rect) for tile in player.world.tile_list)
            if not blocked:
                player.rect.x += movement[0]
                player.update_hitbox()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
       # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def check_collision(self, player_hitbox):
        return self.rect.colliderect(player_hitbox)