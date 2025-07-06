import pygame
import importlib
import os
from player import Player
from objects.exit_tiles import ExitTile
from menu_all.level_menu import LevelCompleteMenu
from menu_all.pause_menu import PauseMenu
from objects.kill_block import Deadly
from menu_all.death_menu import DeathMenu
from objects.benz import RotatingDeadly
from menu_all.final_menu import FinalMenu
from objects.crystal import Crystal
from save_manager import save_progress, load_progress
from objects.enemy import Enemy
from objects.spikes import Spike
from objects.moving_block import MovingBlock
from objects.gun import Gun
from objects.zobast import ToothyEnemy
from objects.stairs import Stair
from objects.gun_item import GunItem
from menu_all.upgrade_menu import load_player_stats

pygame.init()

screen_width = 1300
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Наша игра')

tile_size = 50

moon_img = pygame.image.load('img/moon.png')
bg_img = pygame.image.load('img/background.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

crystal_img = pygame.image.load('img/crystal.png')


def draw_grid():
    for line in range(0, 26):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class World:
    def __init__(self, data, sound_manager):
        self.sound_manager = sound_manager
        self.tile_list = []
        self.exit_tiles = []
        self.deadly_block = []
        self.crystals = []
        self.enemies = []
        self.spikes = []
        self.moving_blocks = []
        self.guns = []
        self.zubast = []
        self.climb_eyes = []
        self.gun_items = []

        tile_imgs = {
            1: 'block_8.png',
            2: 'block_9.png',
            3: 'block_10.png',
            4: 'block_16.png',
            5: 'block_15.png',
            6: 'block_14.png',
            7: 'block_13.png',
            8: 'block_12.png',
            9: 'block_11.png',
            10: 'block_7.png',
            11: 'block_6.png',
            12: 'block_5.png',
            13: 'block_4.png',
            14: 'block_3.png',
            15: 'block_2.png',
            16: 'block_1.png',
            32: 'block_17.png',
            33: 'block_18.png',
            34: 'block_19.png',
            35: 'block_20.png',
            36: 'block_21.png',
            39: 'block_22.png',
            40: 'block_23.png'
        }

        MOVING_BLOCK_TYPES = {
            24: {"size": (50, 50), "direction": "horizontal", "range": 150, "speed": 4, "image": "moving_block.png"},
            37: {"size": (100, 50), "direction": "horizontal", "range": 150, "speed": 4, "image": "moving_block.png"},
            38: {"size": (50, 50), "direction": "horizontal", "range": 150, "speed": 3, "image": "block_21.png"},
            41: {"size": (150, 50), "direction": "horizontal", "range": 200, "speed": 4, "image": "moving_block.png"},
        }

        acid_under_img = pygame.image.load('img/acid_under.png')
        acid_middle_img = pygame.image.load('img/acid_middle.png')
        exit_img = pygame.image.load('img/ext.png')
        crystal_img = pygame.image.load('img/crystal.png')
        saw_img = pygame.image.load('img/benz.png')

        row_count = 0
        for row in data:
            col_count = 0
            for cell in row:
                x = col_count * tile_size
                y = row_count * tile_size
                for tile in cell:
                    if tile in tile_imgs:
                        img = pygame.image.load(f'img/{tile_imgs[tile]}').convert_alpha()
                        img = pygame.transform.scale(img, (tile_size, tile_size))
                        rect = img.get_rect(topleft=(x, y))
                        self.tile_list.append((img, rect))
                    elif tile == 17:
                        self.deadly_block.append(Deadly(x, y, acid_under_img, tile_size))
                    elif tile == 18:
                        self.deadly_block.append(Deadly(x, y, acid_middle_img, tile_size))
                    elif tile == 19:
                        self.exit_tiles.append(ExitTile(x, y, exit_img, tile_size))
                    elif tile == 20:
                        self.deadly_block.append(RotatingDeadly(x, y, saw_img, tile_size, rotation_speed=50))
                    elif tile == 21:
                        self.crystals.append(Crystal(x, y, crystal_img, tile_size))
                    elif tile == 22:
                        self.enemies.append(Enemy(x, y, tile_size))
                    elif tile == 23:
                        self.spikes.append(Spike(x, y, tile_size, self.sound_manager))
                    elif tile == 25:
                        self.guns.append(Gun(x, y, direction='right', sound_manager=sound_manager))
                    elif tile == 26:
                        self.guns.append(Gun(x, y, direction='left', sound_manager=sound_manager))
                    elif tile == 27:
                        self.guns.append(Gun(x, y, direction='up', sound_manager=sound_manager))
                    elif tile == 28:
                        self.guns.append(Gun(x, y, direction='down', sound_manager=sound_manager))
                    elif tile == 29:
                        self.zubast.append(ToothyEnemy(x, y, tile_size, self.sound_manager))
                    elif tile == 30:
                        self.climb_eyes.append(Stair(x, y, tile_size, is_top=True))
                    elif tile == 31:
                        self.climb_eyes.append(Stair(x, y, tile_size, is_top=False))
                    elif tile in MOVING_BLOCK_TYPES:
                        config = MOVING_BLOCK_TYPES[tile]
                        width, height = config["size"]
                        self.moving_blocks.append(MovingBlock(
                            x, y, width, height, direction=config["direction"], move_range=config["range"],
                            speed=config["speed"], image_name=config["image"]))
                    elif tile == 42:
                        self.gun_items.append(GunItem(x, y))
                col_count += 1
            row_count += 1

    def draw(self, screen, player=None, game_active=True):
        for deadly in self.deadly_block:
            if hasattr(deadly, 'update') and game_active:
                deadly.update()
            deadly.draw(screen)
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        for exit_tile in self.exit_tiles:
            if game_active:
                exit_tile.update()
            exit_tile.draw(screen)
        for block in self.moving_blocks:
            if game_active:
                block.update(player)
            block.draw(screen)
        for enemy in self.enemies:
            if game_active:
                enemy.update(self)
            enemy.draw(screen)
        for spike in self.spikes:
            if game_active:
                spike.update()
            spike.draw(screen)
        obstacles = [tile[1] for tile in self.tile_list] + [block.rect for block in self.moving_blocks]
        for gun in self.guns:
            if game_active:
                gun.update(obstacles)
            gun.draw(screen)
        for z in self.zubast:
            if game_active:
                z.update(player.hitbox)
            z.draw(screen)
        for eye in self.climb_eyes:
            eye.draw(screen)
        for crystal in self.crystals:
            if game_active:
                crystal.update()
            crystal.draw(screen)
        for item in self.gun_items:
            item.update()
            item.draw(screen)


def load_level_data(level_number):
    if level_number == "endless":
        level_module = importlib.import_module("levels.level_endless")
    else:
        level_module = importlib.import_module(f"levels.level{level_number}")
    return level_module.world_data


def run_level(screen, level_number, sound_manager, settings_menu):
    level_menu = LevelCompleteMenu(screen_width, screen_height, sound_manager)
    world_data = load_level_data(level_number)
    world = World(world_data, sound_manager)
    final_menu = FinalMenu(screen_width, screen_height, sound_manager)

    sound_manager.play_level_music()
    player = Player(50, screen_height - 130, sound_manager)
    player.world = world

    run = True
    clock = pygame.time.Clock()
    level_menu.hide()

    pause_menu = PauseMenu(screen_width, screen_height, sound_manager)
    paused = False

    player_dead = False

    death_menu = DeathMenu(screen_width, screen_height, sound_manager)
    death_menu.hide()

    total_crystals = len(world.crystals)
    collected_crystals = 0

    levels_folder = "levels"  # Папка с уровнями
    level_files = [f for f in os.listdir(levels_folder) if f.startswith("level") and f.endswith(".py")]
    max_level = len(level_files)

    while run:
        game_active = not paused and not level_menu.visible and not death_menu.visible and not final_menu.visible
        screen.blit(bg_img, (0, 0))
        screen.blit(moon_img, (150, 0))
        world.draw(screen, player, game_active=game_active)

        if not paused and not level_menu.visible and not death_menu.visible and not final_menu.visible:
            player.update(world, screen)
            for item in world.gun_items:
                if not item.picked_up and item.check_collision(player.rect):
                    player.has_gun = True
                    stats = load_player_stats()
                    player.ammo = stats.get("gun_ammo", 5)
            for crystal in world.crystals:
                if crystal.check_collision(player.hitbox):
                    sound_manager.play_effect("cristal")
                    collected_crystals += 1
        else:
            player.draw(screen)

        if not game_active:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

        # Проверка смерти
        if not player_dead and player.check_death(world.deadly_block):
            sound_manager.play_effect("death")
            death_menu.show()
            paused = True
            player_dead = True

        if not player_dead:
            for spike in world.spikes:
                if spike.check_collision(player.hitbox):
                    sound_manager.play_effect("death")
                    death_menu.show()
                    paused = True
                    player_dead = True
                    break

        if not player_dead:
            for gun in world.guns:
                if gun.check_bullet_hits(player.hitbox):
                    sound_manager.play_effect("death")
                    death_menu.show()
                    paused = True
                    player_dead = True
                    break

        if not player_dead:
            for enemy in world.enemies:
                if enemy.check_collision(player.hitbox):
                    sound_manager.play_effect("death")
                    death_menu.show()
                    paused = True
                    player_dead = True
                    break

        if not player_dead:
            for z in world.zubast:
                if z.check_collision(player.hitbox):
                    sound_manager.play_effect("death")
                    death_menu.show()
                    paused = True
                    player_dead = True
                    break

        for bullet in player.bullets:
            for enemy in world.enemies[:]:
                if bullet.rect.colliderect(enemy.hitbox):
                    enemy.take_damage(1)
                    bullet.active = False
                    sound_manager.play_effect("vrag")
                    if enemy.is_dead():
                        world.enemies.remove(enemy)
                    break

        # Проверка выхода
        can_exit = False
        for exit_tile in world.exit_tiles:
            if exit_tile.check_collision(player.rect) and collected_crystals == total_crystals:
                can_exit = True

        # Показываем надпись, если игрок в зоне выхода
        if can_exit and not level_menu.visible and not death_menu.visible and not final_menu.visible and not paused:
            font = pygame.font.SysFont(None, 30)
            text = font.render("Нажмите E, чтобы выйти из уровня", True, (255, 255, 255))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height - 35))

        level_menu.draw(screen)
        pause_menu.draw(screen)
        death_menu.draw(screen)
        final_menu.draw(screen)

       # draw_grid()

        # Количество собранных кристаллов
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Кристаллы: {collected_crystals}/{total_crystals}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

        if player.has_gun:
            font = pygame.font.SysFont(None, 30)
            ammo_text = font.render(f"Патроны: {player.ammo}", True, (255, 255, 0))
            screen.blit(ammo_text, (20, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not level_menu.visible and not death_menu.visible:
                    paused = not paused
                    if paused:
                        pause_menu.show()
                    else:
                        pause_menu.hide()

                if event.key == pygame.K_e and can_exit and not level_menu.visible and not death_menu.visible:
                    sound_manager.play_effect("exit")
                    new_unlocked = level_number + 1
                    current_unlocked = load_progress()
                    if new_unlocked > current_unlocked:
                        save_progress(new_unlocked)

                    if level_number == max_level:
                        final_menu.show()
                    else:
                        level_menu.show()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_menu.visible:
                    result = level_menu.handle_click(event.pos)
                    if result == "menu":
                        return "level_select"
                    elif result == "restart":
                        return f"game_{level_number}"
                    elif result == "next":
                        return f"game_{level_number + 1}"
                elif pause_menu.visible:
                    result = pause_menu.handle_click(event.pos)
                    if result == "resume":
                        paused = False
                        pause_menu.hide()
                    elif result == "restart":
                        return f"game_{level_number}"
                    elif result == "menu":
                        return "level_select"
                    elif result == "settings":
                        running_settings = True
                        settings_menu.show()
                        while running_settings:
                            screen.fill((0, 0, 0))
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    return "exit"
                                result = settings_menu.handle_event(event)
                                if result == "back":
                                    settings_menu.hide()
                                    running_settings = False
                            settings_menu.draw(screen)
                            pygame.display.update()
                            clock.tick(60)
                elif death_menu.visible:
                    result = death_menu.handle_click(event.pos)
                    if result == "restart":
                        death_menu.hide()
                        return f"game_{level_number}"
                    elif result == "menu":
                        death_menu.hide()
                        return "level_select"
                elif final_menu.visible:
                    result = final_menu.handle_click(event.pos)
                    if result == "menu":
                        final_menu.hide()
                        return "level_select"
                    elif result == "restart":
                        final_menu.hide()
                        return f"game_{level_number}"

        pygame.display.update()
        clock.tick(60)
    pygame.quit()