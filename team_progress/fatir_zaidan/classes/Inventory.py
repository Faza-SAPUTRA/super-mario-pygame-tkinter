class Inventory:
    """Stores helper items so purchases can be saved and activated later."""

    def __init__(self):
        self.items = {
            "Mushroom": 0,
            "Star Shield": 0,
            "Super Jump": 0,
            "Enemy Cleaner": 0,
        }

    def addItem(self, itemName):
        self.items[itemName] += 1

    def useItem(self, itemName, action):
        if self.items[itemName] == 0:
            return "You do not have a " + itemName + " in your bag."

        message = action()
        if message.startswith("Cannot"):
            return message

        self.items[itemName] -= 1
        return message

    def getAmount(self, itemName):
        return self.items[itemName]
