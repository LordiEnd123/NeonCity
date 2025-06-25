import pygame
import os


class DeathMenu:
    def __init__(self, screen_width, screen_height, sound_manager):
        self.sound_manager = sound_manager
        self.visible = False

        self.width = 400
        self.height = 200
        self.rect = pygame.Rect(
            (screen_width - self.width) // 2,
            (screen_height - self.height) // 2,
            self.width,
            self.height
        )

        self.font = pygame.font.SysFont('arial', 32, bold=True)
        self.button_font = pygame.font.SysFont('arial', 24, bold=True)
        self.button_font_big = pygame.font.SysFont('arial', 28, bold=True)

        self.menu_bg_img = pygame.image.load(os.path.join("img", "death_menu_bg.png")).convert_alpha()
        self.menu_bg_img = pygame.transform.scale(self.menu_bg_img, (self.width, self.height))

        self.button_img = pygame.image.load(os.path.join("img", "button_red.png")).convert_alpha()
        self.button_img_big = pygame.transform.scale(self.button_img, (220, 48))  # увеличенный для hover

        self.buttons = {
            "restart": pygame.Rect(self.rect.x + 100, self.rect.y + 70, 200, 40),
            "menu": pygame.Rect(self.rect.x + 100, self.rect.y + 130, 200, 40)
        }

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        screen.blit(self.menu_bg_img, self.rect)
        title = self.font.render("Вы умерли", True, (200, 50, 50))
        screen.blit(title, title.get_rect(center=(self.rect.centerx, self.rect.y + 30)))
        labels = {
            "restart": "Переиграть",
            "menu": "Главное меню"
        }

        mouse_pos = pygame.mouse.get_pos()

        for key, rect in self.buttons.items():
            is_hovered = rect.collidepoint(mouse_pos)
            font = self.button_font_big if is_hovered else self.button_font
            if is_hovered:
                scaled_img = self.button_img_big
            else:
                scaled_img = pygame.transform.scale(self.button_img, (rect.width, rect.height))

            scaled_rect = scaled_img.get_rect(center=rect.center)
            screen.blit(scaled_img, scaled_rect)

            text = font.render(labels[key], True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=scaled_rect.center))

    def handle_click(self, pos):
        if not self.visible:
            return None
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.sound_manager.play_effect("click")
                return key
        return None