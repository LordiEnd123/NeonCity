import pygame
import os
from save_manager import load_progress

screen_width = 1300
screen_height = 700


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def run_level_select(screen, sound_manager):
    font = pygame.font.SysFont(None, 50)
    font_big = pygame.font.SysFont(None, 55)
    letters = (50, 205, 50)
    locked_color = (150, 150, 150)
    bg_img = pygame.image.load(os.path.join("img", "new_menu_bg.png"))
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    button_img = pygame.image.load(os.path.join("img", "button_level.png")).convert_alpha()
    button_size = (100, 60)
    button_img = pygame.transform.scale(button_img, button_size)
    back_button_img = pygame.image.load(os.path.join("img", "button_back.png")).convert_alpha()
    back_button_img = pygame.transform.scale(back_button_img, (200, 50))

    buttons = []
    rows, cols = 2, 5
    padding = 30
    btn_w, btn_h = button_size
    start_x = (screen_width - (cols * (btn_w + padding)) + padding) // 2
    start_y = 100

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (btn_w + padding)
            y = start_y + row * (btn_h + padding)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            level_num = row * cols + col + 1
            buttons.append((rect, level_num))

    back_btn = pygame.Rect(screen_width // 2 - 100, 350, 200, 50)

    while True:
        unlocked_levels = load_progress()
        screen.blit(bg_img, (0, 0))
        draw_text("Выбор уровня", font, letters, screen, screen_width // 2, 40)

        mouse_pos = pygame.mouse.get_pos()

        for rect, level in buttons:
            is_unlocked = level <= unlocked_levels
            is_hovered = rect.collidepoint(mouse_pos)

            scale = 1.1 if is_hovered and is_unlocked else 1.0
            new_size = (int(btn_w * scale), int(btn_h * scale))
            scaled_rect = pygame.Rect(
                rect.centerx - new_size[0] // 2,
                rect.centery - new_size[1] // 2,
                new_size[0],
                new_size[1]
            )

            btn_img = pygame.transform.scale(button_img, new_size)
            screen.blit(btn_img, scaled_rect.topleft)

            current_font = font_big if is_hovered else font
            color = letters if is_unlocked else locked_color
            label = current_font.render(str(level), True, color)
            screen.blit(label, label.get_rect(center=scaled_rect.center))

        is_hovered = back_btn.collidepoint(mouse_pos)
        scale = 1.1 if is_hovered else 1.0
        new_back_size = (int(back_btn.width * scale), int(back_btn.height * scale))
        back_rect = pygame.Rect(
            back_btn.centerx - new_back_size[0] // 2,
            back_btn.centery - new_back_size[1] // 2,
            new_back_size[0],
            new_back_size[1]
        )
        back_img = pygame.transform.scale(back_button_img, new_back_size)
        screen.blit(back_img, back_rect.topleft)
        current_font = font_big if is_hovered else font
        back_text = current_font.render("Назад", True, letters)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, level in buttons:
                    if rect.collidepoint(event.pos) and level <= unlocked_levels:
                        sound_manager.play_effect("click")
                        return f"game_{level}"
                if back_btn.collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return "menu"

        pygame.display.update()