class Campaign:
    """Controls the ordered three-level adventure and detects the final ending."""

    def __init__(self):
        self.levelNames = [
            "Level1-1",
            "Level1-2",
            "Level1-3",
        ]
        self.currentIndex = 0

    def getCurrentLevel(self):
        return self.levelNames[self.currentIndex]

    def hasNextLevel(self):
        return self.currentIndex < len(self.levelNames) - 1

    def goToNextLevel(self):
        if self.hasNextLevel() == False:
            return False

        self.currentIndex += 1
        return True

    def getProgressText(self):
        return str(self.currentIndex + 1) + " / " + str(len(self.levelNames))
