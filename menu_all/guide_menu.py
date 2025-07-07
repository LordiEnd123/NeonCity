import pygame
import os

screen_width = 1300
screen_height = 700


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def run_guide_menu(screen):
    font = pygame.font.SysFont(None, 40)
    button_font = pygame.font.SysFont(None, 50)
    button_font_big = pygame.font.SysFont(None, 55)
    letters = (50, 205, 50)

    button_bg_img = pygame.image.load(os.path.join("img", "button_menu.png")).convert_alpha()
    button_bg_img = pygame.transform.scale(button_bg_img, (200, 60))

    bg_img = pygame.image.load(os.path.join("img", "guide_bg.png"))
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    button_rect = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 60)
    button_label = "Назад"

    while True:
        screen.blit(bg_img, (0, 0))
        draw_text("Правила", font, letters, screen, screen_width // 2, 100)

        draw_text("1. Используйте клавиши A, D для движения.", font, letters, screen, screen_width // 2, 200)
        draw_text("2. Нажмите пробел для прыжка.", font, letters, screen, screen_width // 2, 250)
        draw_text("3. Удерживайте Ctrl для ускорения.", font, letters, screen, screen_width // 2, 300)
        draw_text("4. Нажмите W или S, чтобы подняться или спуститься с лестницы.", font, letters, screen, screen_width // 2, 350)
        draw_text("5. Нажмите Shift для того, чтобы слезть с лестницы.", font, letters, screen, screen_width // 2, 400)
        draw_text("6. Стрельба на ЛКМ.", font, letters, screen, screen_width // 2, 450)

        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)
        scale = 1.1 if is_hovered else 1.0

        scaled_width = int(button_rect.width * scale)
        scaled_height = int(button_rect.height * scale)
        scaled_image = pygame.transform.scale(button_bg_img, (scaled_width, scaled_height))
        scaled_rect = scaled_image.get_rect(center=button_rect.center)

        screen.blit(scaled_image, scaled_rect)

        current_font = button_font_big if is_hovered else button_font
        text_surf = current_font.render(button_label, True, letters)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "menu"
        pygame.display.update()