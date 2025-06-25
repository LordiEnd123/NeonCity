import pygame
import os


class Slider:
    def __init__(self, x, y, width, label, value=1.0):
        self.rect = pygame.Rect(x, y, width, 6)
        self.label = label
        self.value = value
        self.handle_radius = 10
        self.dragging = False

    def draw(self, screen, font):
        pygame.draw.line(screen, (180, 180, 180), self.rect.topleft, self.rect.topright, 4)
        handle_x = self.rect.x + int(self.value * self.rect.width)
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, self.rect.centery), self.handle_radius)
        label_text = f"{self.label}: {int(self.value * 100)}"
        text_surface = font.render(label_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x, self.rect.y - 30))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.rect.x + self.value * self.rect.width - self.handle_radius,
                           self.rect.y - self.handle_radius,
                           self.handle_radius * 2,
                           self.handle_radius * 2).collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = min(max(event.pos[0], self.rect.left), self.rect.right)
            self.value = (new_x - self.rect.left) / self.rect.width


class SettingsMenu:
    def __init__(self, screen_width, screen_height, sound_manager):
        self.sound_manager = sound_manager
        self.width = 500
        self.height = 400
        self.rect = pygame.Rect((screen_width - self.width) // 2, (screen_height - self.height) // 2, self.width, self.height)

        self.font = pygame.font.SysFont('arial', 22, bold=True)
        self.title_font = pygame.font.SysFont('arial', 36, bold=True)

        self.sliders = [
            Slider(self.rect.x + 100, self.rect.y + 130, 300, "Общая громкость"),
            Slider(self.rect.x + 100, self.rect.y + 200, 300, "Музыка"),
            Slider(self.rect.x + 100, self.rect.y + 270, 300, "Эффекты"),
        ]
        self.back_button = pygame.Rect(self.rect.centerx - 75, self.rect.y + 310, 150, 45)
        self.visible = False

        self.background_img = pygame.image.load(os.path.join("img", "new_menu_bg.png")).convert()
        self.panel_img = pygame.image.load(os.path.join("img", "level_complete_menu.png")).convert_alpha()
        self.panel_img = pygame.transform.scale(self.panel_img, (self.width, self.height))
        self.back_img = pygame.image.load(os.path.join("img", "button_menu.png")).convert_alpha()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        screen.blit(pygame.transform.scale(self.background_img, screen.get_size()), (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        screen.blit(self.panel_img, self.rect.topleft)
        title = self.title_font.render("Настройки", True, (255, 255, 255))
        screen.blit(title, (self.rect.centerx - title.get_width() // 2, self.rect.y + 40))

        for slider in self.sliders:
            slider.draw(screen, self.font)

        button_scaled = pygame.transform.scale(self.back_img, (self.back_button.width, self.back_button.height))
        screen.blit(button_scaled, self.back_button.topleft)

        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            dark_overlay = pygame.Surface((self.back_button.width, self.back_button.height), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 80))
            screen.blit(dark_overlay, self.back_button.topleft)

        label = self.font.render("Назад", True, (50, 205, 50))
        screen.blit(label, label.get_rect(center=self.back_button.center))

    def handle_event(self, event):
        if not self.visible:
            return None

        for slider in self.sliders:
            slider.handle_event(event)

        self.sound_manager.set_master_volume(self.sliders[0].value)
        self.sound_manager.set_music_volume(self.sliders[1].value)
        self.sound_manager.set_effects_volume(self.sliders[2].value)
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.collidepoint(event.pos):
            self.sound_manager.play_effect("click")
            return "back"
        return None

    def get_volumes(self):
        return {
            "master": self.sliders[0].value,
            "music": self.sliders[1].value,
            "effects": self.sliders[2].value,
        }