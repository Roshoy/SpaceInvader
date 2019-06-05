import pygame


class SoundManager:
    music_volume = 0.3
    sound_volume = 0.6

    player_hit_sound = None
    bomb_explosion_sound = None
    laser_shot_sound = None
    player_explosion_sound = None
    rocket_shot_sound = None

    def __init__(self):
        SoundManager.player_hit_sound = pygame.mixer.Sound("./Sounds/chamber_decompressing.wav")
        SoundManager.player_hit_sound.set_volume(SoundManager.sound_volume)
        SoundManager.bomb_explosion_sound = pygame.mixer.Sound("./Sounds/bomb_explosion.wav")
        SoundManager.bomb_explosion_sound.set_volume(SoundManager.sound_volume)
        SoundManager.laser_shot_sound = pygame.mixer.Sound("./Sounds/laser_shot.wav")
        SoundManager.laser_shot_sound.set_volume(SoundManager.sound_volume)
        SoundManager.player_explosion_sound = pygame.mixer.Sound("./Sounds/player_explosion.wav")
        SoundManager.player_explosion_sound.set_volume(SoundManager.sound_volume)
        SoundManager.rocket_shot_sound = pygame.mixer.Sound("./Sounds/rocket_shot.wav")
        SoundManager.rocket_shot_sound.set_volume(SoundManager.sound_volume)

    @staticmethod
    def change_volume(volume: float):
        if volume < 0 or volume > 1:
            return
        pygame.mixer.music.set_volume(volume/2)
        SoundManager.player_hit_sound.set_volume(volume)
        SoundManager.bomb_explosion_sound.set_volume(volume)
        SoundManager.laser_shot_sound.set_volume(volume)
        SoundManager.player_explosion_sound.set_volume(volume)
        SoundManager.rocket_shot_sound.set_volume(volume)

    @staticmethod
    def play_music():
        pygame.mixer.music.load('./Sounds/battle.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(SoundManager.music_volume)

    @staticmethod
    def sound_player_hit():
        SoundManager.player_hit_sound.play(0, 0, 1)

    @staticmethod
    def sound_bomb_explosion():
        SoundManager.bomb_explosion_sound.play(0, 0, 1)

    @staticmethod
    def sound_laser_shot():
        SoundManager.laser_shot_sound.play(0, 0, 1)

    @staticmethod
    def sound_player_explosion():
        SoundManager.player_explosion_sound.play(0, 0, 1)

    @staticmethod
    def sound_rocket_shot():
        SoundManager.rocket_shot_sound.play(0, 0, 1)

    @staticmethod
    def sound_rocket_shot_stop():
        SoundManager.rocket_shot_sound.stop()
