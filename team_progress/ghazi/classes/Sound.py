from pygame import mixer


class Sound:
    def __init__(self, settings):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(settings["musicVolume"] / 100)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(settings["sfxVolume"] / 100)

        self.allowSFX = settings["sfx"]

        self.soundtrack = mixer.Sound("./sfx/main_theme.ogg")
        self.coin = mixer.Sound("./sfx/coin.ogg")
        self.bump = mixer.Sound("./sfx/bump.ogg")
        self.stomp = mixer.Sound("./sfx/stomp.ogg")
        self.jump = mixer.Sound("./sfx/small_jump.ogg")
        self.death = mixer.Sound("./sfx/death.wav")
        self.kick = mixer.Sound("./sfx/kick.ogg")
        self.brick_bump = mixer.Sound("./sfx/brick-bump.ogg")
        self.powerup = mixer.Sound('./sfx/powerup.ogg')
        self.powerup_appear = mixer.Sound('./sfx/powerup_appears.ogg')
        self.pipe = mixer.Sound('./sfx/pipe.ogg')

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music, loops=-1):
        self.music_channel.play(music, loops=loops)
