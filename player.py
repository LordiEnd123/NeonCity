import pygame
import os
from stats import PlayerStatsManager
from objects.bullet import BulletPlayer


class Player:
    def __init__(self, x, y, sound_manager):
        self.sound_manager = sound_manager
        self.load_images()
        self.on_stair_top = False

        self.facing_right = True
        self.image_index = 0
        self.image = self.idle_image
        self.animation_counter = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.hitbox_offset_left = 22
        self.hitbox_offset_right = 22
        self.hitbox_offset_top = 25
        self.hitbox_offset_bottom = 1

        self.vel_y = 0
        self.jump_pressed = False
        self.in_air = True
        self.ducking = False
        self.speed = 5

        self.climbing = False
        self.ready_to_climb = False
        self.climbing_direction = None

        # Инициализация менеджера характеристик
        self.stats_manager = PlayerStatsManager()

        # Время с начала игры
        self.last_time = pygame.time.get_ticks()  # Время в миллисекундах

        # Инициализация ускорения
        self.accelerating = False
        self.alpha = 0  # Прозрачность полоски (начинаем с 0, то есть полностью прозрачна)

        self.has_gun = False

        self.bullets = []
        self.shoot_cooldown = 300  # мс
        self.last_shot_time = 0

        self.ammo = 0

        self.update_hitbox()

    def load_images(self):
        self.walk_images = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"hero_{i}.png")), (80, 80)) for i in range(3, 5)]
        self.idle_image = pygame.transform.scale(pygame.image.load("img/hero_1.png"), (80, 80))
        self.jump_image = pygame.transform.scale(pygame.image.load("img/hero_2.png"), (80, 80))
        self.duck_images = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"hero_{i}.png")), (80, 80)) for i in range(5, 7)]
        self.climb_up_images = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"hero_{i}.png")), (80, 80)) for i in range(7, 9)]
        self.climb_down_images = self.climb_up_images

        # С пистолетом
        self.walk_images_gun = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"gun_hero_{i}.png")), (80, 80)) for i in range(3, 5)]
        self.idle_image_gun = pygame.transform.scale(pygame.image.load("img/gun_hero_1.png"), (80, 80))
        self.jump_image_gun = pygame.transform.scale(pygame.image.load("img/gun_hero_2.png"), (80, 80))
        self.duck_images_gun = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"gun_hero_{i}.png")), (80, 80)) for i in range(5, 7)]
        self.climb_up_images_gun = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"gun_hero_{i}.png")), (80, 80)) for i in range(7, 9)]
        self.climb_down_images_gun = self.climb_up_images_gun

    def update_hitbox(self):
        if self.ducking:
            hitbox_height = 50
            top_offset = 30
        else:
            hitbox_height = self.rect.height - self.hitbox_offset_top - self.hitbox_offset_bottom
            top_offset = self.hitbox_offset_top

        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset_left, self.rect.y + top_offset,
            self.rect.width - self.hitbox_offset_left - self.hitbox_offset_right, hitbox_height)

    def handle_input(self, keys, world):
        self.dx = 0
        self.dy = 0
        self.moving = False
        self.climbing_direction = None

        # Получаем текущее время
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0  # delta_time в секундах

        # Обновляем время для следующего кадра
        self.last_time = current_time

        # Логика ускорения (при удержании Ctrl)
        if keys[pygame.K_LCTRL] and self.stats_manager.get_stat("stamina") > 0:
            self.accelerating = True  # Ускорение
            self.speed = 6.5  # Увеличиваем скорость при ускорении
        else:
            self.accelerating = False  # Без ускорения
            self.speed = 5  # Обычная скорость

        # Обновляем выносливость в зависимости от движения и ускорения
        if keys[pygame.K_d] or keys[pygame.K_a]:
            self.moving = True
            self.stats_manager.update_stamina(self.moving, self.accelerating, delta_time)
        else:
            # Если игрок не двигается, восстанавливаем выносливость
            self.stats_manager.update_stamina(self.moving, self.accelerating, delta_time)

        # Плавное изменение прозрачности полоски (затухание)
        if self.accelerating:
            self.alpha = min(self.alpha + 10 * delta_time, 255)  # Увеличиваем прозрачность
        else:
            self.alpha = max(self.alpha - 10 * delta_time, 0)  # Уменьшаем прозрачность

        self.update_hitbox()

        # Проверка, есть ли лестница под игроком
        self.ready_to_climb = False
        self.climb_eye = None
        for eye in world.climb_eyes:
            if eye.check_player_inside(self.hitbox):
                self.ready_to_climb = True
                self.climb_eye = eye
                break

        # Если мы на лестнице, но уже не в её зоне, то отключаем лазание
        if self.climbing:
            if not self.climb_eye or not self.climb_eye.rect.colliderect(self.hitbox):
                self.climbing = False
                self.climbing_direction = None
                self.climb_eye = None

        # Начало подъема по клавише
        if self.ready_to_climb and (keys[pygame.K_w] or keys[pygame.K_s]):
            if not (self.climb_eye and self.climb_eye.is_top and keys[pygame.K_SPACE]):
                self.climbing = True
                self.rect.centerx = self.climb_eye.rect.centerx

        if self.climbing and keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.climbing = False
            self.climbing_direction = None

        if self.climbing:
            # Проверка, если вышли за пределы лестницы, то отключаем взбирание
            if not self.climb_eye.rect.colliderect(self.hitbox):
                self.climbing = False
                self.climbing_direction = None
            else:
                self.vel_y = 0
                self.in_air = False
                if keys[pygame.K_w]:
                    self.dy = -3
                    self.climbing_direction = "up"
                elif keys[pygame.K_s]:
                    self.dy = 3
                    self.climbing_direction = "down"
                else:
                    self.dy = 0
                self.dx = 0

        else:
            # Обработка обычного управления
            if keys[pygame.K_s] and not self.in_air:
                self.ducking = True
            elif not keys[pygame.K_s] and self.ducking:
                test_hitbox = pygame.Rect(
                    self.rect.x + self.hitbox_offset_left,
                    self.rect.y + self.hitbox_offset_top,
                    self.rect.width - self.hitbox_offset_left - self.hitbox_offset_right,
                    self.rect.height - self.hitbox_offset_top - self.hitbox_offset_bottom
                )
                can_stand = not any(tile[1].colliderect(test_hitbox) for tile in world.tile_list)
                if can_stand:
                    self.ducking = False

            current_speed = self.speed * 0.4 if self.ducking else self.speed

            if keys[pygame.K_a]:
                self.dx -= current_speed
                self.facing_right = False
                self.moving = True
            if keys[pygame.K_d]:
                self.dx += current_speed
                self.facing_right = True
                self.moving = True

            if keys[pygame.K_SPACE] and not self.jump_pressed and not self.in_air and not self.on_stair_top and not self.ducking:
                self.vel_y = -15
                self.jump_pressed = True
                self.sound_manager.play_effect("jump")
            if not keys[pygame.K_SPACE]:
                self.jump_pressed = False

            if keys[pygame.K_f] and self.has_gun:
                now = pygame.time.get_ticks()
                if now - self.last_shot_time > self.shoot_cooldown:
                    self.shoot()
                    self.last_shot_time = now

        self.update_hitbox()

    def apply_physics(self):
        if not self.climbing:
            self.vel_y += 1
            self.vel_y = min(self.vel_y, 10)
            self.dy += self.vel_y
        else:
            self.vel_y = 0

    def shoot(self):
        if self.ammo > 0:
            bullet_x = self.rect.right if self.facing_right else self.rect.left
            bullet_y = self.rect.centery
            direction = 1 if self.facing_right else -1
            self.bullets.append(BulletPlayer(bullet_x, bullet_y, direction, self.sound_manager))
            self.ammo -= 1

    def check_collisions(self, world):
        self.in_air = not self.climbing
        collision_rects = world.tile_list + [(None, block.rect) for block in world.moving_blocks]
        for z in world.zubast:
            z_rect = z.rect.copy()
            z_rect.height -= 10
            z_rect.top += 10
            collision_rects.append((None, z_rect))

        for tile in collision_rects:
            tile_rect = tile[1]
            if tile_rect.colliderect(self.hitbox.x + self.dx, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                self.dx = 0
            if tile_rect.colliderect(self.hitbox.x, self.hitbox.y + self.dy, self.hitbox.width, self.hitbox.height):
                if self.vel_y < 0:
                    self.dy = tile_rect.bottom - self.hitbox.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = tile_rect.top - self.hitbox.bottom
                    self.vel_y = 0
                    self.in_air = False

        # Если стоим на верхней ступеньке лестницы, то не падаем
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_s]:
            for stair in world.climb_eyes:
                if stair.player_on_top(self.hitbox):
                    self.in_air = False
                    self.vel_y = 0
                    self.dy = 0
                    self.climbing = False
                    break

        self.on_stair_top = False
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_s]:
            for stair in world.climb_eyes:
                if stair.player_on_top(self.hitbox):
                    self.in_air = False
                    self.vel_y = 0
                    self.dy = 0
                    self.climbing = False
                    self.on_stair_top = True
                    break

    def update_animation(self):
        if self.has_gun:
            if self.climbing:
                if self.climbing_direction in ("up", "down"):
                    self.animation_counter += 1
                    if self.animation_counter >= 10:
                        self.animation_counter = 0
                        self.image_index = (self.image_index + 1) % len(self.climb_up_images_gun)
                    self.image = self.climb_up_images_gun[self.image_index]
                else:
                    self.image = self.climb_up_images_gun[0]
            elif self.in_air:
                self.image = self.jump_image_gun
            elif self.ducking:
                if self.moving:
                    self.animation_counter += 1
                    if self.animation_counter >= 10:
                        self.animation_counter = 0
                        self.image_index = (self.image_index + 1) % len(self.duck_images_gun)
                    self.image = self.duck_images_gun[self.image_index]
                else:
                    self.image = self.duck_images_gun[0]
            elif self.moving:
                self.animation_counter += 1
                if self.animation_counter >= 10:
                    self.animation_counter = 0
                    self.image_index = (self.image_index + 1) % len(self.walk_images_gun)
                self.image = self.walk_images_gun[self.image_index]
            else:
                self.image = self.idle_image_gun
        else:
            if self.climbing:
                if self.climbing_direction in ("up", "down"):
                    self.animation_counter += 1
                    if self.animation_counter >= 10:
                        self.animation_counter = 0
                        self.image_index = (self.image_index + 1) % len(self.climb_up_images)
                    self.image = self.climb_up_images[self.image_index]
                else:
                    self.image = self.climb_up_images[0]
            elif self.in_air:
                self.image = self.jump_image
            elif self.ducking:
                if self.moving:
                    self.animation_counter += 1
                    if self.animation_counter >= 10:
                        self.animation_counter = 0
                        self.image_index = (self.image_index + 1) % len(self.duck_images)
                    self.image = self.duck_images[self.image_index]
                else:
                    self.image = self.duck_images[0]
            elif self.moving:
                self.animation_counter += 1
                if self.animation_counter >= 10:
                    self.animation_counter = 0
                    self.image_index = (self.image_index + 1) % len(self.walk_images)
                self.image = self.walk_images[self.image_index]
            else:
                self.image = self.idle_image

    def update(self, world, screen):
        # Вызов handle_input без необходимости передавать delta_time напрямую
        keys = pygame.key.get_pressed()
        self.handle_input(keys, world)
        self.apply_physics()
        self.check_collisions(world)

        self.rect.x += self.dx
        self.rect.y += self.dy
        self.update_hitbox()
        self.update_animation()
        self.draw(screen)

        for bullet in self.bullets:
            bullet.update(world)
        self.bullets = [b for b in self.bullets if b.active]

    def draw(self, screen):
        flipped = pygame.transform.flip(self.image, True, False) if not self.facing_right else self.image
        screen.blit(flipped, self.rect)

        # Рисуем полоску ускорения
        self.draw_acceleration_bar(screen)
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_acceleration_bar(self, screen):
        """Отображаем полоску ускорения над персонажем"""

        # Проверяем, активен ли ускорение
        if self.accelerating:
            # Получаем процент оставшейся выносливости
            stamina_percentage = self.stats_manager.get_stat("stamina") / self.stats_manager.max_stamina

            # Размеры полоски
            bar_width = 50  # Уменьшаем ширину полоски
            bar_height = 6  # Меньше высота полоски
            bar_x = self.rect.centerx - bar_width / 2
            bar_y = self.rect.top + 8  # Немного опускаем полоску для лучшего отображения

            # Темно-желтый цвет для полоски
            full_color = (255, 204, 0)  # Темно-желтый цвет
            empty_color = (204, 153, 0)  # Темный желтый цвет для пустой части полоски

            # Рисуем пустую полоску (темнее)
            pygame.draw.rect(screen, empty_color, (bar_x, bar_y, bar_width, bar_height))

            # Рисуем заполненную часть полоски (освещенная)
            pygame.draw.rect(screen, full_color, (bar_x, bar_y, bar_width * stamina_percentage, bar_height))


    def check_death(self, deadly_acids):
        for acid in deadly_acids:
            if acid.check_collision(self.hitbox):
                self.sound_manager.play_effect("death")
                return True
        return False

    def check_zubast_death(self, zubast_list):
        for z in zubast_list:
            if z.check_collision(self.hitbox):
                self.sound_manager.play_effect("death")
                return True
        return False
