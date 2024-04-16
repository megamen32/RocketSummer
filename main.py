from gamemanager import manager

if __name__ == '__main__':
    while manager.current_day < manager.days_to_survive:
        manager.player_action()