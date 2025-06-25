import pygame
import os


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

        self.update_hitbox()

    def load_images(self):
        self.walk_images = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"hero_{i}.png")), (80, 80)) for i in range(3, 5)]
        self.idle_image = pygame.transform.scale(pygame.image.load("img/hero_1.png"), (80, 80))
        self.jump_image = pygame.transform.scale(pygame.image.load("img/hero_2.png"), (80, 80))
        self.duck_images = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"hero_{i}.png")), (80, 80)) for i in range(5, 7)]
        self.climb_up_images = [pygame.transform.scale(pygame.image.load(os.path.join("img", f"hero_{i}.png")), (80, 80)) for i in range(7, 9)]
        self.climb_down_images = self.climb_up_images

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

        self.update_hitbox()

    def apply_physics(self):
        if not self.climbing:
            self.vel_y += 1
            self.vel_y = min(self.vel_y, 10)
            self.dy += self.vel_y
        else:
            self.vel_y = 0

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
        keys = pygame.key.get_pressed()
        self.handle_input(keys, world)
        self.apply_physics()
        self.check_collisions(world)

        self.rect.x += self.dx
        self.rect.y += self.dy
        self.update_hitbox()
        self.update_animation()
        self.draw(screen)

    def draw(self, screen):
        flipped = pygame.transform.flip(self.image, True, False) if not self.facing_right else self.image
        screen.blit(flipped, self.rect)
      #  pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

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
