PROGRESS_OWNER = "Kala"
DIFFICULTY_LEVEL = "Beginner"

MAIN_FEATURES = [
    "Coin placement review",
    "Enemy placement review",
    "Three-level campaign map checking",
    "Manual playthrough checklist",
]

TOUCHED_AREAS = [
    "levels/Level1-1.json",
    "levels/Level1-2.json",
    "levels/Level1-3.json",
]

MANUAL_TESTS = [
    "Mario can finish World 1-1",
    "Mario can finish World 1-2",
    "Mario can finish World 1-3",
    "Coins and enemies are reachable during normal gameplay",
]


def get_progress():
    return {
        "owner": PROGRESS_OWNER,
        "difficulty": DIFFICULTY_LEVEL,
        "features": MAIN_FEATURES,
        "areas": TOUCHED_AREAS,
        "manual_tests": MANUAL_TESTS,
    }
