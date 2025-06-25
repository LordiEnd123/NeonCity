import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.8
        self.effects_volume = 0.8
        self.master_volume = 0.8
        self.current_music = None

        self.sounds = {
            "jump": pygame.mixer.Sound("sounds/jump.mp3"),
            "death": pygame.mixer.Sound("sounds/death.mp3"),
            "click": pygame.mixer.Sound("sounds/click.mp3"),
            "exit": pygame.mixer.Sound("sounds/exit.wav"),
            "cristal": pygame.mixer.Sound("sounds/cristal.mp3"),
            "gun": pygame.mixer.Sound("sounds/gun.mp3"),
            "spikes": pygame.mixer.Sound("sounds/spikes.mp3")
        }

        self.menu_music = "sounds/menu_music.wav"
        self.level_music = "sounds/level_soun.mp3"

    def play_menu_music(self):
        if self.current_music == self.menu_music and pygame.mixer.music.get_busy():
            return
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        pygame.mixer.music.play(-1)
        self.current_music = self.menu_music

    def play_level_music(self):
        if self.current_music == self.level_music and pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(self.level_music)
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        pygame.mixer.music.play(-1)
        self.current_music = self.level_music

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_effect(self, name):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(self.effects_volume * self.master_volume)
            sound.play()

    def set_master_volume(self, volume):
        self.master_volume = volume
        pygame.mixer.music.set_volume(self.music_volume * volume)

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume * self.master_volume)

    def set_effects_volume(self, volume):
        self.effects_volume = volume