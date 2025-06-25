import pygame
from menu_all.menu import run_menu
from menu_all.level_select import run_level_select
from world import run_level
from settings.settings_menu import SettingsMenu
from settings.sound_manager import SoundManager

screen_width = 1300
screen_height = 700

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Наша игра")

clock = pygame.time.Clock()
game_state = "menu"

sound_manager = SoundManager()
sound_manager.play_menu_music()

settings_menu = SettingsMenu(screen_width, screen_height, sound_manager)

running = True
while running:
    if game_state == "menu":
        sound_manager.play_menu_music()
        game_state = run_menu(screen, sound_manager)

    elif game_state == "level_select":
        game_state = run_level_select(screen, sound_manager)

    elif game_state.startswith("game_"):
        level_number = int(game_state.split("_")[1])
        game_state = run_level(screen, level_number, sound_manager, settings_menu)
        if game_state in ("menu", "level_select"):
            sound_manager.play_menu_music()

    elif game_state == "settings":
        running_settings = True
        settings_menu.show()
        while running_settings:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    running_settings = False
                    break
                result = settings_menu.handle_event(event)
                if result == "back":
                    game_state = "menu"
                    running_settings = False
            settings_menu.draw(screen)
            pygame.display.update()
            clock.tick(60)

    elif game_state == "exit":
        running = False

    clock.tick(60)

pygame.quit()