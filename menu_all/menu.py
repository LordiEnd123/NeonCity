import pygame
import os
from menu_all.guide_menu import run_guide_menu  # Импортируем меню Руководства

screen_width = 1300
screen_height = 700


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def run_menu(screen, sound_manager):
    font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 50)
    button_font_big = pygame.font.SysFont(None, 55)
    letters = (50, 205, 50)

    button_bg_img = pygame.image.load(os.path.join("img", "button_menu.png")).convert_alpha()
    button_bg_img = pygame.transform.scale(button_bg_img, (200, 60))

    bg_img = pygame.image.load(os.path.join("img", "new_menu_bg.png"))
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    base_buttons = {
        "play": pygame.Rect(screen_width // 2 - 100, 200, 200, 60),
        "settings": pygame.Rect(screen_width // 2 - 100, 300, 200, 60),
        "guide": pygame.Rect(screen_width // 2 - 100, 400, 200, 60),  # Добавляем кнопку Руководства
        "quit": pygame.Rect(screen_width // 2 - 100, 500, 200, 60)
    }

    labels = {
        "play": "Играть",
        "settings": "Настройки",
        "guide": "Правила",  # Надпись на кнопке Руководства
        "quit": "Выход"
    }

    while True:
        screen.blit(bg_img, (0, 0))
        draw_text("NEON CITY", font, letters, screen, screen_width // 2, 100)

        mouse_pos = pygame.mouse.get_pos()

        for key, rect in base_buttons.items():
            is_hovered = rect.collidepoint(mouse_pos)
            scale = 1.1 if is_hovered else 1.0

            scaled_width = int(rect.width * scale)
            scaled_height = int(rect.height * scale)
            scaled_image = pygame.transform.scale(button_bg_img, (scaled_width, scaled_height))
            scaled_rect = scaled_image.get_rect(center=rect.center)

            screen.blit(scaled_image, scaled_rect)

            current_font = button_font_big if is_hovered else button_font
            text_surf = current_font.render(labels[key], True, letters)
            text_rect = text_surf.get_rect(center=scaled_rect.center)
            screen.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if base_buttons["play"].collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return "level_select"
                elif base_buttons["settings"].collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return "settings"
                elif base_buttons["guide"].collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return run_guide_menu(screen)
                elif base_buttons["quit"].collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return "exit"

        pygame.display.update()