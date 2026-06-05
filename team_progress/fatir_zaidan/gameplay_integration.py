PROGRESS_OWNER = "Fatir Zaidan"
DIFFICULTY_LEVEL = "Advanced"

MAIN_FEATURES = [
    "Pygame main loop integration",
    "Three-level campaign flow",
    "Mario gameplay upgrades",
    "Shop, inventory, quest, and checkpoint integration",
    "Final debugging before presentation",
]

TOUCHED_AREAS = [
    "main.py",
    "entities/Mario.py",
    "classes/Level.py",
    "classes/Campaign.py",
    "classes/Shop.py",
    "classes/Inventory.py",
    "classes/QuestTracker.py",
    "classes/CheckpointManager.py",
]


def get_progress():
    return {
        "owner": PROGRESS_OWNER,
        "difficulty": DIFFICULTY_LEVEL,
        "features": MAIN_FEATURES,
        "areas": TOUCHED_AREAS,
    }
