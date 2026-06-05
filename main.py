import pygame

from classes.Campaign import Campaign
from classes.Dashboard import Dashboard
from classes.Launcher import Launcher
from classes.Level import Level
from classes.Sound import Sound
from entities.Mario import Mario


windowSize = 640, 480
maxFrameRate = 60
settingsUrl = "./settings.json"


def openLauncher():
    launcher = Launcher(settingsUrl)
    return launcher.open()


def setupGame(settings):
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    displayFlags = 0
    if settings["fullscreen"]:
        displayFlags = pygame.FULLSCREEN

    screen = pygame.display.set_mode(windowSize, displayFlags)
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound(settings)
    if settings["sound"]:
        sound.play_music(sound.soundtrack)

    level = Level(screen, sound, dashboard)

    return screen, dashboard, sound, level


def loadLevel(levelName, dashboard, level):
    level.loadLevel(levelName)
    dashboard.state = "start"
    dashboard.levelName = levelName.replace("Level", "")


def playCampaign(screen, dashboard, sound, level):
    campaign = Campaign()
    loadLevel(campaign.getCurrentLevel(), dashboard, level)

    mario = Mario(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()

    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))

        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()

        if mario.levelCompleted:
            dashboard.points += 1000

            if campaign.goToNextLevel():
                showLevelCompleted(screen, dashboard, campaign.getCurrentLevel())
                loadLevel(campaign.getCurrentLevel(), dashboard, level)
                mario.prepareNextLevel()
            else:
                showCampaignCompleted(screen, dashboard)
                return

        pygame.display.update()
        clock.tick(maxFrameRate)


def showLevelCompleted(screen, dashboard, nextLevel):
    clock = pygame.time.Clock()

    while True:
        dashboard.drawText("LEVEL COMPLETE", 150, 190, 24)
        dashboard.drawText("NEXT " + nextLevel.replace("Level", ""), 225, 235, 18)
        dashboard.drawText("PRESS ENTER", 190, 270, 18)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        clock.tick(maxFrameRate)


def showCampaignCompleted(screen, dashboard):
    clock = pygame.time.Clock()

    while True:
        screen.fill((92, 148, 252))
        dashboard.drawText("YOU WIN", 220, 155, 34)
        dashboard.drawText("ALL 3 LEVELS COMPLETE", 105, 220, 20)
        dashboard.drawText("PRESS ENTER", 190, 280, 18)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        clock.tick(maxFrameRate)


def main():
    while True:
        settings = openLauncher()
        if settings is None:
            return

        screen, dashboard, sound, level = setupGame(settings)
        playCampaign(screen, dashboard, sound, level)
        pygame.quit()


if __name__ == "__main__":
    main()
