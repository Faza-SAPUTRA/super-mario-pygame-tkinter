import sys
from pathlib import Path

from pygame import mixer


class Sound:
    def __init__(self, settings):
        if mixer.get_init() is None:
            mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

        if getattr(sys, "frozen", False):
            app_root = Path(sys.executable).resolve().parent
        else:
            app_root = Path(__file__).resolve().parent.parent

        def load(filename):
            return mixer.Sound(str(app_root / "sfx" / filename))

        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(self._volume(settings["musicVolume"]))
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(self._volume(settings["sfxVolume"]))

        self.allowSFX = settings["sfx"]

        self.soundtrack = load("main_theme.ogg")
        self.coin = load("coin.ogg")
        self.bump = load("bump.ogg")
        self.stomp = load("stomp.ogg")
        self.jump = load("small_jump.ogg")
        self.death = load("death.wav")
        self.kick = load("kick.ogg")
        self.brick_bump = load("brick-bump.ogg")
        self.powerup = load("powerup.ogg")
        self.powerup_appear = load("powerup_appears.ogg")
        self.pipe = load("pipe.ogg")

    @staticmethod
    def _volume(value):
        return max(0, min(100, float(value))) / 100

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music, loops=-1):
        self.music_channel.play(music, loops=loops)
