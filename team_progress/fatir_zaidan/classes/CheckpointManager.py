class CheckpointManager:
    """Keeps one paid checkpoint and restores Mario after a dangerous fall."""

    def __init__(self, mario):
        self.mario = mario
        self.active = False
        self.x = 0
        self.y = 0

    def activate(self):
        self.x = self.mario.rect.x
        self.y = self.mario.rect.y
        self.active = True
        return "Checkpoint saved at your current position."

    def restore(self):
        if self.active == False:
            return False

        self.mario.rect.x = self.x
        self.mario.rect.y = self.y
        self.mario.vel.x = 0
        self.mario.vel.y = 0
        self.mario.invincibilityFrames = 180
        self.active = False
        return True

    def getStatus(self):
        if self.active:
            return "ACTIVE"

        return "NOT SET"

    def reset(self):
        self.active = False
