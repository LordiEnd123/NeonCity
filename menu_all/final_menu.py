import pygame
import os


class FinalMenu:
    def __init__(self, screen_width, screen_height, sound_manager):
        self.sound_manager = sound_manager
        self.width = 500
        self.height = 300
        self.rect = pygame.Rect((screen_width - self.width) // 2, (screen_height - self.height) // 2, self.width, self.height)

        self.font = pygame.font.SysFont('arial', 32, bold=True)
        self.button_font = pygame.font.SysFont('arial', 24, bold=True)
        self.button_font_big = pygame.font.SysFont('arial', 28, bold=True)
        self.visible = False

        self.bg_image = pygame.image.load(os.path.join("img", "level_complete_menu.png")).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        self.button_img = pygame.image.load(os.path.join("img", "button_level.png")).convert_alpha()
        self.button_size = (200, 40)

        self.buttons = {
            "restart": pygame.Rect(self.rect.x + 150, self.rect.y + 130, 200, 40),
            "menu": pygame.Rect(self.rect.x + 150, self.rect.y + 180, 200, 40)
        }

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        screen.blit(self.bg_image, self.rect.topleft)
        title = self.font.render("Поздравляем!", True, (50, 205, 50))
        subtitle = self.button_font.render("Вы прошли все уровни!", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(self.rect.centerx, self.rect.y + 40)))
        screen.blit(subtitle, subtitle.get_rect(center=(self.rect.centerx, self.rect.y + 80)))
        mouse_pos = pygame.mouse.get_pos()
        labels = {
            "restart": "Переиграть",
            "menu": "Главное меню"
        }

        for key, rect in self.buttons.items():
            is_hovered = rect.collidepoint(mouse_pos)
            scale = 1.1 if is_hovered else 1.0
            new_size = (int(self.button_size[0] * scale), int(self.button_size[1] * scale))
            scaled_rect = pygame.Rect(rect.centerx - new_size[0] // 2, rect.centery - new_size[1] // 2, new_size[0], new_size[1])

            scaled_button = pygame.transform.scale(self.button_img, new_size)
            screen.blit(scaled_button, scaled_rect.topleft)
            font = self.button_font_big if is_hovered else self.button_font
            text_surf = font.render(labels[key], True, (50, 205, 50))
            screen.blit(text_surf, text_surf.get_rect(center=scaled_rect.center))

    def handle_click(self, pos):
        if not self.visible:
            return None
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if self.sound_manager:
                    self.sound_manager.play_effect("click")
                return key
        return None