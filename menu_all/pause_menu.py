import pygame
import os


class PauseMenu:
    def __init__(self, screen_width, screen_height, sound_manager):
        self.sound_manager = sound_manager
        self.width = 400
        self.height = 280
        self.rect = pygame.Rect((screen_width - self.width) // 2, (screen_height - self.height) // 2, self.width, self.height)

        self.font = pygame.font.SysFont('arial', 22, bold=True)
        self.button_font = pygame.font.SysFont('arial', 24, bold=True)
        self.button_font_big = pygame.font.SysFont('arial', 28, bold=True)
        self.visible = False

        self.bg_image = pygame.image.load(os.path.join("img", "in_level.png")).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        self.button_image = pygame.image.load(os.path.join("img", "button_menu.png")).convert_alpha()
        self.button_size = (200, 40)

        self.buttons = {
            "resume": pygame.Rect(self.rect.x + 100, self.rect.y + 60, 200, 40),
            "restart": pygame.Rect(self.rect.x + 100, self.rect.y + 110, 200, 40),
            "settings": pygame.Rect(self.rect.x + 100, self.rect.y + 160, 200, 40),
            "menu": pygame.Rect(self.rect.x + 100, self.rect.y + 210, 200, 40),
        }

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        screen.blit(self.bg_image, self.rect.topleft)
        title = self.font.render("Пауза", True, (50, 205, 50))
        screen.blit(title, title.get_rect(center=(self.rect.centerx, self.rect.y + 30)))

        labels = {
            "resume": "Продолжить",
            "restart": "Переиграть",
            "settings": "Настройки",
            "menu": "Главное меню"
        }

        mouse_pos = pygame.mouse.get_pos()

        for key, rect in self.buttons.items():
            is_hovered = rect.collidepoint(mouse_pos)
            scale = 1.1 if is_hovered else 1.0

            new_w = int(self.button_size[0] * scale)
            new_h = int(self.button_size[1] * scale)
            scaled_rect = pygame.Rect(rect.centerx - new_w // 2, rect.centery - new_h // 2, new_w, new_h)

            button_img_scaled = pygame.transform.scale(self.button_image, (new_w, new_h))
            screen.blit(button_img_scaled, scaled_rect.topleft)

            font = self.button_font_big if is_hovered else self.button_font
            text_surface = font.render(labels[key], True, (50, 205, 50))
            screen.blit(text_surface, text_surface.get_rect(center=scaled_rect.center))

    def handle_click(self, pos):
        if not self.visible:
            return None
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.sound_manager.play_effect("click")
                return key
        return None