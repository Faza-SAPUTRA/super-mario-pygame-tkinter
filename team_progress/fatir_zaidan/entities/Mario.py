import pygame

from classes.Animation import Animation
from classes.Camera import Camera
from classes.CheckpointManager import CheckpointManager
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Inventory import Inventory
from classes.QuestTracker import QuestTracker
from classes.Sprites import Sprites
from entities.EntityBase import EntityBase
from entities.Mushroom import RedMushroom
from traits.bounce import bounceTrait
from traits.go import GoTrait
from traits.jump import JumpTrait
from classes.Pause import Pause
from classes.Shop import Shop

spriteCollection = Sprites().spriteCollection
smallAnimation = Animation(
    [
        spriteCollection["mario_run1"].image,
        spriteCollection["mario_run2"].image,
        spriteCollection["mario_run3"].image,
    ],
    spriteCollection["mario_idle"].image,
    spriteCollection["mario_jump"].image,
)
bigAnimation = Animation(
    [
        spriteCollection["mario_big_run1"].image,
        spriteCollection["mario_big_run2"].image,
        spriteCollection["mario_big_run3"].image,
    ],
    spriteCollection["mario_big_idle"].image,
    spriteCollection["mario_big_jump"].image,
)


class Mario(EntityBase):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8):
        super(Mario, self).__init__(x, y, gravity)
        self.camera = Camera(self.rect, self)
        self.sound = sound
        self.input = Input(self)
        self.inAir = False
        self.inJump = False
        self.powerUpState = 0
        self.invincibilityFrames = 0
        self.traits = {
            "jumpTrait": JumpTrait(self),
            "goTrait": GoTrait(smallAnimation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self),
        }

        self.levelObj = level
        self.collision = Collider(self, level)
        self.screen = screen
        self.EntityCollider = EntityCollider(self)
        self.dashboard = dashboard
        self.restart = False
        self.levelCompleted = False
        self.pause = False
        self.pauseObj = Pause(screen, self, dashboard)
        # Composition: Mario owns helper systems instead of mixing their logic into one class.
        self.inventory = Inventory()
        self.checkpoints = CheckpointManager(self)
        self.quests = QuestTracker(dashboard)
        self.shopMessage = ""

    def update(self):
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
        self.updateTraits()
        self.moveMario()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.checkFinishFlag()
        self.input.checkForInput()

    def checkFinishFlag(self):
        if self.levelObj.hasMarioReachedFinishFlag(self.rect):
            self.levelCompleted = True
            self.vel.x = 0

    def tryUsePipe(self):
        destination = self.levelObj.findPipeWarp(self.rect)
        if destination is None:
            return

        exitX, exitY = destination
        self.sound.play_sfx(self.sound.pipe)
        self.rect.x = exitX * 32
        self.rect.bottom = exitY * 32
        self.vel.x = 0
        self.vel.y = 0
        self.invincibilityFrames = max(self.invincibilityFrames, 60)
        self.camera.move()
        self.shopMessage = "Warp pipe used. Mario found a shortcut."

    def prepareNextLevel(self):
        """Resets map-specific state while preserving inventory, quests, and coins."""
        height = 32
        if self.powerUpState == 1:
            height = 64

        self.rect = pygame.Rect(0, 0, 32, height)
        self.camera = Camera(self.rect, self)
        self.traits["goTrait"].camera = self.camera
        self.collision = Collider(self, self.levelObj)
        self.EntityCollider = EntityCollider(self)
        self.checkpoints.reset()
        self.levelCompleted = False
        self.pause = False
        self.pauseObj = Pause(self.screen, self, self.dashboard)
        self.vel.x = 0
        self.vel.y = 0

    def openShop(self):
        Shop(self).open()

    def spendCoins(self, price):
        if self.dashboard.coins < price:
            return False

        self.dashboard.coins -= price
        return True

    def buyMushroom(self):
        return self.buyInventoryItem("Mushroom", 5)

    def buyShield(self):
        return self.buyInventoryItem("Star Shield", 8)

    def buySuperJump(self):
        return self.buyInventoryItem("Super Jump", 3)

    def buyEnemyCleaner(self):
        return self.buyInventoryItem("Enemy Cleaner", 10)

    def buyInventoryItem(self, itemName, price):
        if self.spendCoins(price) == False:
            return "Not enough coins for a " + itemName + "."

        self.inventory.addItem(itemName)
        questMessage = self.quests.record("shop")
        return itemName + " added to your bag. " + questMessage

    def buyCheckpoint(self):
        if self.spendCoins(6) == False:
            return "Not enough coins for a Checkpoint."

        return self.checkpoints.activate()

    def useMushroom(self):
        return self.inventory.useItem("Mushroom", self.activateMushroom)

    def useShield(self):
        return self.inventory.useItem("Star Shield", self.activateShield)

    def useSuperJump(self):
        return self.inventory.useItem("Super Jump", self.activateSuperJump)

    def useEnemyCleaner(self):
        return self.inventory.useItem("Enemy Cleaner", self.activateEnemyCleaner)

    def activateMushroom(self):
        if self.powerUpState == 1:
            return "Cannot use Mushroom: Mario is already powered up."

        self.powerup(1)
        return "Mushroom activated. Mario is bigger now."

    def activateShield(self):
        self.invincibilityFrames = max(self.invincibilityFrames, 600)
        return "Star Shield activated for 10 seconds."

    def activateSuperJump(self):
        self.vel.y = -16
        self.inAir = True
        self.inJump = False
        self.obeyGravity = True
        return "Super Jump activated."

    def activateEnemyCleaner(self):
        removedEnemies = 0

        for entity in self.levelObj.entityList:
            distance = abs(entity.rect.x - self.rect.x)

            if entity.type == "Mob" and distance <= 6 * 32:
                entity.alive = False
                removedEnemies += 1

        return "Enemy Cleaner removed " + str(removedEnemies) + " nearby enemies."

    def moveMario(self):
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithItem(self, item):
        self.levelObj.entityList.remove(item)
        self.dashboard.points += 100
        self.dashboard.coins += 1
        self.shopMessage = self.quests.record("coin")
        self.sound.play_sfx(self.sound.coin)

    def _onCollisionWithBlock(self, block):
        if not block.triggered:
            self.dashboard.coins += 1
            self.shopMessage = self.quests.record("coin")
            self.sound.play_sfx(self.sound.bump)
        block.triggered = True

    def _onCollisionWithMob(self, mob, collisionState):
        if isinstance(mob, RedMushroom) and mob.alive:
            self.powerup(1)
            self.killEntity(mob)
            self.sound.play_sfx(self.sound.powerup)
        elif collisionState.isTop and (mob.alive or mob.bouncing):
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.killEntity(mob)
        elif collisionState.isTop and mob.alive and not mob.active:
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            mob.timer = 0
            self.bounce()
            mob.alive = False
        elif collisionState.isColliding and mob.alive and not mob.active and not mob.bouncing:
            mob.bouncing = True
            if mob.rect.x < self.rect.x:
                mob.leftrightTrait.direction = -1
                mob.rect.x += -5
                self.sound.play_sfx(self.sound.kick)
            else:
                mob.rect.x += 5
                mob.leftrightTrait.direction = 1
                self.sound.play_sfx(self.sound.kick)
        elif collisionState.isColliding and mob.alive and not self.invincibilityFrames:
            if self.powerUpState == 0:
                self.gameOver()
            elif self.powerUpState == 1:
                self.powerUpState = 0
                self.traits['goTrait'].updateAnimation(smallAnimation)
                x, y = self.rect.x, self.rect.y
                self.rect = pygame.Rect(x, y + 32, 32, 32)
                self.invincibilityFrames = 60
                self.sound.play_sfx(self.sound.pipe)

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent):
        if ent.__class__.__name__ != "Koopa":
            ent.alive = False
        else:
            ent.timer = 0
            ent.leftrightTrait.speed = 1
            ent.alive = True
            ent.active = False
            ent.bouncing = False
        self.dashboard.points += 100
        if isinstance(ent, RedMushroom) == False:
            self.shopMessage = self.quests.record("enemy")

    def gameOver(self):
        if self.checkpoints.restore():
            self.shopMessage = "Checkpoint restored. Mario is back in the action."
            return

        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.sound.music_channel.stop()
        self.sound.music_channel.play(self.sound.death)

        for i in range(500, 20, -2):
            srf.fill((0, 0, 0))
            pygame.draw.circle(
                srf,
                (255, 255, 255),
                (int(self.camera.x + self.rect.x) + 16, self.rect.y + 16),
                i,
            )
            self.screen.blit(srf, (0, 0))
            pygame.display.update()
            self.input.checkForInput()
        while self.sound.music_channel.get_busy():
            pygame.display.update()
            self.input.checkForInput()
        self.restart = True

    def getPos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def powerup(self, powerupID):
        if self.powerUpState == 0:
            if powerupID == 1:
                self.powerUpState = 1
                self.traits['goTrait'].updateAnimation(bigAnimation)
                self.rect = pygame.Rect(self.rect.x, self.rect.y-32, 32, 64)
                self.invincibilityFrames = 20
