PROGRESS_OWNER = "Rafa Rabbani"
DIFFICULTY_LEVEL = "Beginner"

MAIN_FEATURES = [
    "README feature summary",
    "Control guide wording",
    "UI asset loading support",
    "Presentation demo flow preparation",
]

TOUCHED_AREAS = [
    "README.md",
    "classes/UiAssets.py",
    "img/title_screen.png",
    "img/characters.gif",
    "img/Items.png",
]

DEMO_FLOW = [
    "Open launcher",
    "Show level selector and audio settings",
    "Start campaign",
    "Open shop with B",
    "Show inventory, quest, and checkpoint flow",
]


def get_progress():
    return {
        "owner": PROGRESS_OWNER,
        "difficulty": DIFFICULTY_LEVEL,
        "features": MAIN_FEATURES,
        "areas": TOUCHED_AREAS,
        "demo_flow": DEMO_FLOW,
    }
