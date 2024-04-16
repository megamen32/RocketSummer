from gamemanager import manager
import time

def end_game(self):
    manager.check_endings()
    exit()

if __name__ == '__main__':
    print("Лето 2024:")
    time.sleep(1)
    print(
        "Это было лето 2014. Я только что закончила школу и думала, что это будет лучшее лето в моей жизни. Все казалось идеальным, когда я пошла на речку с подругой.")
    time.sleep(2)
    print("Но вдруг мне позвонили и сказали, что объявлена воздушная тревога. Мой мир рухнул в одно мгновение.")
    time.sleep(1)
    print(
        "Я побежала домой, по дороге встречая испуганные лица. Дома на меня уже ждала моя семья, взволнованная, но вместе. Мы не знали, что будет дальше, но знали, что должны держаться вместе.")
    time.sleep(1)
    print("Так началось наше выживание...")

    while manager.current_day < manager.days_to_survive:
        manager.player_action()


    end_game()