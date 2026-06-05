PROGRESS_OWNER = "Ghazi"
DIFFICULTY_LEVEL = "Beginner to middle"

MAIN_FEATURES = [
    "Tkinter launcher window",
    "Level selector preview",
    "Audio toggle and volume settings",
    "Fullscreen option",
    "Controls guide tab",
]

TOUCHED_AREAS = [
    "classes/Launcher.py",
    "classes/Sound.py",
    "classes/UiAssets.py",
    "requirements.txt",
]


def get_progress():
    return {
        "owner": PROGRESS_OWNER,
        "difficulty": DIFFICULTY_LEVEL,
        "features": MAIN_FEATURES,
        "areas": TOUCHED_AREAS,
    }
