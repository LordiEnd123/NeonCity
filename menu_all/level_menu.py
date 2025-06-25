import pygame
import os


class LevelCompleteMenu:
    def __init__(self, screen_width, screen_height, sound_manager):
        self.sound_manager = sound_manager
        self.width = 400
        self.height = 300
        self.rect = pygame.Rect(
            (screen_width - self.width) // 2,
            (screen_height - self.height) // 2,
            self.width,
            self.height
        )

        self.font = pygame.font.SysFont('arial', 32, bold=True)
        self.button_font = pygame.font.SysFont('arial', 24, bold=True)
        self.button_font_big = pygame.font.SysFont('arial', 28, bold=True)
        self.visible = False

        self.bg_image = pygame.image.load(os.path.join("img", "in_level.png")).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        self.button_image = pygame.image.load(os.path.join("img", "button_menu.png")).convert_alpha()
        self.button_image = pygame.transform.scale(self.button_image, (200, 40))

        self.buttons = {
            "next": pygame.Rect(self.rect.x + 80, self.rect.y + 80, 250, 40),
            "restart": pygame.Rect(self.rect.x + 80, self.rect.y + 130, 250, 40),
            "menu": pygame.Rect(self.rect.x + 80, self.rect.y + 180, 250, 40)
        }

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        screen.blit(self.bg_image, self.rect.topleft)
        title = self.font.render("Уровень пройден!", True, (50, 205, 50))
        screen.blit(title, title.get_rect(center=(self.rect.centerx, self.rect.y + 40)))

        labels = {
            "next": "Следующий уровень",
            "restart": "Переиграть",
            "menu": "Главное меню"
        }

        mouse_pos = pygame.mouse.get_pos()
        for key, rect in self.buttons.items():
            is_hovered = rect.collidepoint(mouse_pos)
            scale = 1.1 if is_hovered else 1.0

            new_w = int(rect.width * scale)
            new_h = int(rect.height * scale)
            scaled_rect = pygame.Rect(
                rect.centerx - new_w // 2,
                rect.centery - new_h // 2,
                new_w,
                new_h
            )

            scaled_img = pygame.transform.scale(self.button_image, (new_w, new_h))
            screen.blit(scaled_img, scaled_rect.topleft)

            font = self.button_font_big if is_hovered else self.button_font
            label_surface = font.render(labels[key], True, (50, 205, 50))
            screen.blit(label_surface, label_surface.get_rect(center=scaled_rect.center))

    def handle_click(self, pos):
        if not self.visible:
            return None
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.sound_manager.play_effect("click")
                return key
        return None