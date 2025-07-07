import pygame


class BulletPlayer:
    bullet_img = None

    def __init__(self, x, y, direction, sound_manager, speed=10):
        if BulletPlayer.bullet_img is None:
            BulletPlayer.bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
            BulletPlayer.bullet_img = pygame.transform.scale(BulletPlayer.bullet_img, (20, 8))

        self.image = BulletPlayer.bullet_img
        self.rect = self.image.get_rect(center=(x, y + 20))
        self.direction = direction
        self.speed = speed
        self.active = True
        sound_manager.play_effect("gun")

    def update(self, world):
        self.rect.x += self.speed * self.direction
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.active = False
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)