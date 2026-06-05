class Quest:
    """Represents one optional challenge and the coin reward it grants."""

    def __init__(self, title, description, target, reward):
        self.title = title
        self.description = description
        self.target = target
        self.reward = reward
        self.progress = 0
        self.completed = False

    def addProgress(self, amount=1):
        if self.completed:
            return 0

        self.progress += amount
        if self.progress >= self.target:
            self.progress = self.target
            self.completed = True
            return self.reward

        return 0


class QuestTracker:
    """Observes gameplay events and pays coin rewards for completed quests."""

    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.quests = {
            "coin": Quest("Coin Hunter", "Collect 8 coins in one run.", 8, 4),
            "enemy": Quest("Stomp Squad", "Defeat 3 enemies.", 3, 5),
            "shop": Quest("Smart Shopper", "Buy 2 helper items.", 2, 3),
        }

    def record(self, questName, amount=1):
        reward = self.quests[questName].addProgress(amount)
        if reward > 0:
            self.dashboard.coins += reward
            return "Quest completed! +" + str(reward) + " bonus coins."

        return ""

    def getQuests(self):
        return list(self.quests.values())
