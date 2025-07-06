import pygame
import os
import json

CONFIG_PATH = "config_stats.json"
SAVE_PATH = "save_data.json"
STATS_FILE = "config_stats.json"


def load_save_data():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as file:
            data = json.load(file)
            if "spent_points" not in data:
                data["spent_points"] = 0
            return data
    return {"unlocked_levels": 1, "spent_points": 0}


def load_player_stats():
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_player_stats(data):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def run_upgrade_menu(screen, sound_manager):
    pygame.font.init()
    font = pygame.font.SysFont("arial", 30, bold=True)
    big_font = pygame.font.SysFont("arial", 44, bold=True)

    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()

    save_data = load_save_data()
    available_points = max(0, save_data["unlocked_levels"] - 1 - save_data.get("spent_points", 0))

    stats = load_player_stats()
    upgraded_stats = stats.copy()

    stat_box_height = 80
    stat_box_width = 700
    base_y = 150

    button_image = pygame.image.load(os.path.join("img", "button_menu.png")).convert_alpha()
    button_image = pygame.transform.scale(button_image, (200, 50))
    back_btn_rect = pygame.Rect(screen_width // 2 - 100, 580, 200, 50)

    bg_image = pygame.image.load(os.path.join("img", "guide_bg.png")).convert()
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

    points_spent_now = 0

    stat_labels = {
        "max_stamina": "Максимальная выносливость",
        "stamina_regeneration_rate": "Восстановление выносливости",
        "gun_ammo": "Патроны в оружии"
    }

    upgrade_buttons = {
        key: pygame.Rect(900, base_y + i * (stat_box_height + 20) + 20, 40, 40)
        for i, key in enumerate(stat_labels)
    }

    running = True
    while running:
        screen.fill((25, 25, 30))
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        draw_text("Прокачка персонажа", big_font, (255, 255, 255), screen, screen_width // 2, 70)
        draw_text(f"Очки прокачки: {available_points}", font, (255, 215, 0), screen, screen_width // 2, 120)

        # Отрисовка каждого параметра
        for i, (key, label) in enumerate(stat_labels.items()):
            y = base_y + i * (stat_box_height + 20)

            # Подложка под параметры
            box_rect = pygame.Rect(300, y, stat_box_width, stat_box_height)
            pygame.draw.rect(screen, (40, 40, 50), box_rect, border_radius=12)
            pygame.draw.rect(screen, (100, 100, 120), box_rect, 2, border_radius=12)

            # Название и значение
            draw_text(f"{label}: {round(upgraded_stats[key], 2)}", font, (255, 255, 255), screen, box_rect.centerx - 80, box_rect.centery)

            # Кнопка "+"
            mouse_over = upgrade_buttons[key].collidepoint(mouse_pos)
            plus_color = (0, 120, 0) if mouse_over else (0, 160, 0)
            pygame.draw.rect(screen, plus_color, upgrade_buttons[key], border_radius=6)
            draw_text("+", font, (255, 255, 255), screen, upgrade_buttons[key].centerx, upgrade_buttons[key].centery)

        # Кнопка назад с ховер-анимацией
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = back_btn_rect.collidepoint(mouse_pos)
        scale = 1.1 if is_hovered else 1.0
        new_w = int(back_btn_rect.width * scale)
        new_h = int(back_btn_rect.height * scale)
        scaled_rect = pygame.Rect(back_btn_rect.centerx - new_w // 2, back_btn_rect.centery - new_h // 2, new_w, new_h)
        scaled_image = pygame.transform.scale(button_image, (new_w, new_h))
        screen.blit(scaled_image, scaled_rect.topleft)

        back_font = big_font if is_hovered else font
        draw_text("Назад", back_font, (50, 205, 50), screen, scaled_rect.centerx, scaled_rect.centery)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn_rect.collidepoint(event.pos):
                    sound_manager.play_effect("click")
                    save_player_stats(upgraded_stats)
                    save_data["spent_points"] += points_spent_now
                    with open(SAVE_PATH, "w") as f:
                        json.dump(save_data, f, indent=4)
                    return "level_select"

                for stat_key, btn_rect in upgrade_buttons.items():
                    if btn_rect.collidepoint(event.pos) and available_points > 0:
                        if stat_key == "max_stamina":
                            upgraded_stats[stat_key] += 2.5
                        elif stat_key == "stamina_regeneration_rate":
                            upgraded_stats[stat_key] += 0.5
                        elif stat_key == "gun_ammo":
                            upgraded_stats[stat_key] += 1
                        available_points -= 1
                        points_spent_now += 1
                        sound_manager.play_effect("upgrad")