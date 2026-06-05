from team_progress.fatir_zaidan.gameplay_integration import get_progress as fatir_progress
from team_progress.ghazi.launcher_settings import get_progress as ghazi_progress
from team_progress.kala.level_balancing import get_progress as kala_progress
from team_progress.rafa_rabbani.ui_presentation import get_progress as rafa_progress


def print_section(progress):
    print(progress["owner"] + " - " + progress["difficulty"])
    print("Features:")
    for feature in progress["features"]:
        print("- " + feature)

    print("Areas:")
    for area in progress["areas"]:
        print("- " + area)
    print()


def main():
    for progress in [
        fatir_progress(),
        ghazi_progress(),
        kala_progress(),
        rafa_progress(),
    ]:
        print_section(progress)


if __name__ == "__main__":
    main()
