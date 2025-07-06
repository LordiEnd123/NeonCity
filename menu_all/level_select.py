import os
import pygame
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
    levels_per_page = 20
    current_page = 0

    bg_img = pygame.image.load(os.path.join("img", "new_menu_bg.png"))
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    button_img = pygame.image.load(os.path.join("img", "button_level.png")).convert_alpha()
    button_size = (100, 60)

    back_button_img = pygame.image.load(os.path.join("img", "button_back.png")).convert_alpha()
    back_button_img = pygame.transform.scale(back_button_img, (200, 50))

    arrow_img = pygame.image.load(os.path.join("img", "strelka_right.png")).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (60, 60))

    hover_sound_played = {"next": False, "prev": False}

    # Получаем список всех файлов уровней в папке
    levels_folder = "levels"
    level_files = [f for f in os.listdir(levels_folder) if f.startswith("level") and f.endswith(".py")]
    max_level = len(level_files)

    def create_level_buttons(start_level, end_level):
        buttons = []
        rows, cols = 4, 5
        padding = 30
        btn_w, btn_h = button_size
        start_x = (screen_width - (cols * (btn_w + padding)) + padding) // 2
        start_y = 100

        level = start_level
        for row in range(rows):
            for col in range(cols):
                if level > end_level:
                    break
                x = start_x + col * (btn_w + padding)
                y = start_y + row * (btn_h + padding)
                rect = pygame.Rect(x, y, btn_w, btn_h)
                buttons.append((rect, level))
                level += 1
        return buttons

    back_btn = pygame.Rect(screen_width // 2 - 100, 610, 200, 50)
    next_arrow = pygame.Rect(screen_width - 100, 610, 60, 60)
    prev_arrow = pygame.Rect(40, 610, 60, 60)

    # Кнопка Прокачка (над кнопкой Назад)
    upgrade_btn = pygame.Rect(screen_width // 2 - 100, 540, 200, 50)
    upgrade_button_img = pygame.transform.scale(back_button_img, (200, 50))

    while True:
        screen.blit(bg_img, (0, 0))
        draw_text("Выбор уровня", font, letters, screen, screen_width // 2, 40)

        page_start = current_page * levels_per_page + 1
        page_end = min(page_start + levels_per_page - 1, max_level)
        buttons = create_level_buttons(page_start, page_end)

        mouse_pos = pygame.mouse.get_pos()

        for rect, level in buttons:
            is_unlocked = level <= load_progress()
            is_hovered = rect.collidepoint(mouse_pos)

            scale = 1.1 if is_hovered and is_unlocked else 1.0
            new_size = (int(button_size[0] * scale), int(button_size[1] * scale))
            scaled_rect = pygame.Rect(rect.centerx - new_size[0] // 2, rect.centery - new_size[1] // 2, new_size[0], new_size[1])

            btn_img = pygame.transform.scale(button_img, new_size)
            screen.blit(btn_img, scaled_rect.topleft)

            current_font = font_big if is_hovered else font
            color = letters if is_unlocked else locked_color
            label = current_font.render(str(level), True, color)
            screen.blit(label, label.get_rect(center=scaled_rect.center))

        # Назад
        is_hovered = back_btn.collidepoint(mouse_pos)
        scale = 1.1 if is_hovered else 1.0
        new_size = (int(back_btn.width * scale), int(back_btn.height * scale))
        back_rect = pygame.Rect(back_btn.centerx - new_size[0] // 2, back_btn.centery - new_size[1] // 2, new_size[0], new_size[1])
        back_img = pygame.transform.scale(back_button_img, new_size)
        screen.blit(back_img, back_rect.topleft)
        back_text = (font_big if is_hovered else font).render("Назад", True, letters)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

        is_hovered = upgrade_btn.collidepoint(mouse_pos)
        scale = 1.1 if is_hovered else 1.0
        new_size = (int(upgrade_btn.width * scale), int(upgrade_btn.height * scale))
        upgrade_rect = pygame.Rect(upgrade_btn.centerx - new_size[0] // 2, upgrade_btn.centery - new_size[1] // 2, new_size[0], new_size[1])
        upgrade_img = pygame.transform.scale(upgrade_button_img, new_size)
        screen.blit(upgrade_img, upgrade_rect.topleft)
        upgrade_text = (font_big if is_hovered else font).render("Прокачка", True, letters)
        screen.blit(upgrade_text, upgrade_text.get_rect(center=upgrade_rect.center))

        # Стрелки
        if current_page < (max_level - 1) // levels_per_page:
            hovered = next_arrow.collidepoint(mouse_pos)
            if hovered and not hover_sound_played["next"]:
                sound_manager.play_effect("hover")
                hover_sound_played["next"] = True
            elif not hovered:
                hover_sound_played["next"] = False

            scale = 1.2 if hovered else 1.0
            arrow_scaled = pygame.transform.scale(arrow_img, (int(60 * scale), int(60 * scale)))
            arrow_pos = (
                next_arrow.centerx - arrow_scaled.get_width() // 2,
                next_arrow.centery - arrow_scaled.get_height() // 2
            )
            screen.blit(arrow_scaled, arrow_pos)

        if current_page > 0:
            hovered = prev_arrow.collidepoint(mouse_pos)
            if hovered and not hover_sound_played["prev"]:
                sound_manager.play_effect("hover")
                hover_sound_played["prev"] = True
            elif not hovered:
                hover_sound_played["prev"] = False

            arrow_flipped = pygame.transform.flip(arrow_img, True, False)
            scale = 1.2 if hovered else 1.0
            arrow_scaled = pygame.transform.scale(arrow_flipped, (int(60 * scale), int(60 * scale)))
            arrow_pos = (prev_arrow.centerx - arrow_scaled.get_width() // 2, prev_arrow.centery - arrow_scaled.get_height() // 2)
            screen.blit(arrow_scaled, arrow_pos)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, level in buttons:
                    if rect.collidepoint(event.pos) and level <= load_progress():
                        sound_manager.play_effect("click")
                        return f"game_{level}"
                if back_rect.collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return "menu"
                if upgrade_rect.collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    return "upgrade_menu"
                if next_arrow.collidepoint(event.pos) and current_page < (max_level - 1) // levels_per_page:
                    current_page += 1
                if prev_arrow.collidepoint(event.pos) and current_page > 0:
                    current_page -= 1

        pygame.display.update()