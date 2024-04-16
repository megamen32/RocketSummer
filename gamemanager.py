import random
import time
from typing import List

from character import Character
from food_storage import FoodStorage,all_food
from house import House


class GameManager:
    def __init__(self):
        self.current_hour = 1
        self.hours_in_a_day = 5  # Максимум действий, которые могут выполнить персонажи; одно действие занимает 1 час.
        self.current_day = 1
        self.days_to_survive = 20
        self.characters = [Character(self,"Мама",8), Character(self,"Папа",10), Character(self,"Брат",4), Character(self,"Ты",6)]
        self.food_storage = FoodStorage(self)
        self.fuel_storage = FoodStorage(self,'Гараж')
        self.house = House(self)
        self.today_action_perfomed=0
        self.max_action_to_perform=lambda :max(1, len([hero for hero in self.characters if hero.can_act()]))
        self.today_can_perform_actions = self.max_action_to_perform()
        self.news = [
            "Местные власти сообщают об ухудшении погодных условий.",
            "В новостях объявили о возможных перебоях с электричеством из-за ближайших боев.",
            "Соседний город подвергся массированной атаке. Жители в панике.",
            "Гуманитарная помощь скоро должна прибыть в ближайшие дни.",
            "Вчера вечером был сбит вражеский беспилотник над городом.",
            "Мирные переговоры начнутся в следующую неделю, сообщают источники.",
            "Жители города организуют общественную оборону."
        ]


    def broadcast_news(self):
        # Выбор случайной новости из списка
        news_of_the_day = random.choice(self.news)
        print(f"Новости дня: {news_of_the_day}")

    def new_day(self):
        self.check_elictricity()
        self.current_hour = 1
        self.current_day += 1
        self.today_action_perfomed = 0
        self.today_can_perform_actions=self.max_action_to_perform()
        for food in all_food:
            food.new_day()
        self.house.generator.new_day()
        self.broadcast_news()
        for character in self.characters:
           if character.health<=3:
               damage=random.randint(0,1)/2
               if damage:
                  character.take_damage(damage)


    def perform_action(self, character_index, action_type):
        if self.today_action_perfomed >= self.today_can_perform_actions:
            print("Сегодня активные действия у персонажей закончились")
            return False
        if self.today_action_perfomed >= self.hours_in_a_day:
            print("Уже наступила ночь и ничего не видно")
            return False
        character = self.characters[character_index]

        print(f'{character.name} пытается {action_type}')
        result = False
        if character.dead:
            print(f'{character.name} умер')
        else:
            if action_type == "покушать":
                result = character.feed(self.food_storage)
            elif action_type == 'выйти из подвала':
                result = character.return_from_basement()
            else:
                if not character.can_act():
                    print(f"{character.name} не может действовать.")
                    return False
                if action_type == "собрать ресурсы":
                    resource=int(input('Что искать? 1-искать еду, 2 - искать топливо? :'))
                    if resource==1:
                        resource='еда'
                        storage=self.food_storage
                    elif resource==2:
                        resource='топливо'
                        storage=self.fuel_storage
                    result = character.gather_food(storage,resource_type=resource)
                elif action_type == "починить дом":
                    result = self.house.repair()
                elif action_type =='починить холодильник':
                    result=self.food_storage.repair()
                elif action_type =='починить генератор':
                    result=self.fuel_storage.repair()
                elif action_type == 'спрятаться в подвал':
                    result =character.hide_in_basement()
                elif action_type == 'включить генератор':
                    result = self.house.generator.turn_on()
                elif action_type == 'выключить генератор':
                    result = self.house.generator.turn_off()
                elif action_type=='выкинуть мусор':
                    result=self.food_storage.clear_trash()


        if result:
            self.today_action_perfomed += 1
            self.current_hour += 1
            self.check_bombardment()
            for character in self.characters:
                character.reset_actions()  # Сброс количества выполненных действий
        return result

    def check_bombardment(self):
        if random.random() < 0.15:  # 10% шанс на обстрел каждый час
            self.house.bombard()


            print('-----------------------')
            time.sleep(0.2)
            print("\tПрилет! Дом и персонажи получили урон.")
            for character in self.characters:
                if character.in_basement():
                    continue
                if character.location!='В доме':
                    continue

                damage = random.randint(0, 2)
                if damage>0:
                    character.take_damage(damage)
            time.sleep(0.5)
            if self.house.durability<90:
                if random.random()<0.3:
                    self.food_storage._hp=0
                    print('Холодильник выведен из строя')
                if random.random() < 0.3:
                    self.fuel_storage._hp = 0
                    print('Гараж выведен из строя')
            print('💥')
    def check_elictricity(self):
        if self.house.electricity_from_outside and random.random()<0.2:
            print('-----------------------')
            time.sleep(0.2)
            self.house.electricity_from_outside=False
            print('\tОтключили электричество!')
            return
        if not self.house.electricity_from_outside and random.random()<0.6:
            print('-----------------------')
            self.house.electricity_from_outside = True
            print('\tЭлектричество снова дали!')

            return


    def display_status(self):
        print(f"День: {self.current_day}/{self.days_to_survive}, Час: {self.current_hour}/{self.hours_in_a_day}, Активных Действий: {self.today_action_perfomed}/{self.today_can_perform_actions}")
        for i,character in enumerate(self.characters):
            if character.dead:
                continue
            print('\t\t',i+1,character)
        print(self.house)

    def player_action(self):
        self.display_status()
        action_performed = False
        while not action_performed:
            end=self.check_end_day()
            if end:
                break
            character_choice=-1
            while character_choice<0 or character_choice>len(self.characters):
                try:
                    character_choice = int(input("Выбери персонажа (1-4): "))
                except:
                    print('Введите число от 1 до 4')


            if self.characters[character_choice-1].in_basement():
                input_action_txt = 'Выбери действие (выйти из подвала-7'
            else:
                input_action_txt = f"Выбери действие (покушать-1, собрать ресурсы-2, починить дом-3, проверить холодильник-4 "
                if  self.food_storage._hp==0:
                    input_action_txt += ', починить холодильник-5'
                if  self.fuel_storage._hp==0:
                    input_action_txt += ', починить генератор-11'

                input_action_txt+=', спрятаться в подвал-6'
                if not self.house.generator.is_turned_on:
                    can_turn_on_generator=not self.house.electricity_from_outside
                    if can_turn_on_generator:
                        if not self.house.generator.is_turned_on_and_working():
                            input_action_txt+=', включить генератор-9'
                if self.house.generator.is_turned_on:
                        input_action_txt += ', выключить генератор-0'
                input_action_txt+=', проверить гараж - 8'
            input_action_txt+='):'

            action_choice = input(input_action_txt)
            try:
                action_choice=int(action_choice)
                if action_choice==1:
                    action_choice='покушать'
                elif action_choice==2:
                    action_choice='собрать ресурсы'
                elif action_choice==3:
                    action_choice='починить дом'
                elif action_choice==4:
                    action_choice = 'проверить холодильник'
                elif action_choice==5:
                    action_choice='починить холодильник'
                elif action_choice==6:
                    action_choice='спрятаться в подвал'
                elif action_choice==7:
                    action_choice = 'выйти из подвала'
                elif action_choice==8:
                    action_choice = 'проверить гараж'
                elif action_choice==9:
                    action_choice = 'включить генератор'
                elif action_choice==0:
                    action_choice = 'выключить генератор'
                elif action_choice==11:
                    action_choice='починить генератор'
            except:
                pass
            if action_choice=='проверить холодильник':
                self.food_storage.status()
                if any([food.is_expired for food in self.food_storage.food ]):
                    trash_out=int(input("Выкинуть мусор? 1-да, 2-нет"))
                    if trash_out==1:
                        action_performed=self.perform_action(character_choice - 1, 'выкинуть мусор')
                    else:
                        action_performed=True
            elif action_choice=='проверить гараж':
                self.fuel_storage.status()
                action_performed=True
            else:
                action_performed = self.perform_action(character_choice-1, action_choice)
        if self.check_end_day():
            for i in range(self.hours_in_a_day-self.current_hour):
                self.check_bombardment()
            print("Конец дня")
            self.new_day()
            time.sleep(1)

    def check_end_day(self):
        if self.current_hour > self.hours_in_a_day or self.today_action_perfomed >= self.today_can_perform_actions:

            return True
        return False

    def check_endings(self):
        alive_count = sum(not char.dead for char in self.characters)
        total_count = len(self.characters)

        print("Конец игры.")
        print(f"Выжило {alive_count} из {total_count} членов семьи.")
        good_end = True
        if alive_count == total_count:
            print(
                "Все члены семьи выжили. Вы блестяще справились с испытаниями и сумели сохранить свою семью в целости и безопасности.")
        elif alive_count >= total_count // 2:
            print(
                "Большинство членов вашей семьи выжило. Несмотря на потери, вы смогли сохранить ядро семьи и теперь впереди у вас время для восстановления и взаимопомощи.")
        elif alive_count > 0:
            print(
                "Выжило несколько членов семьи. Потери огромны, и это оставит след в ваших сердцах, но вы должны идти дальше.")
        else:
            print(
                "Никто не выжил. Ваша история заканчивается здесь, в трагедии и разрушении. Это напоминает о жестокости ситуации, с которой вы столкнулись.")
            good_end = False
        if good_end:
            print("Вы смогли выжить 20 дней в условиях бесконечных испытаний и неопределенности.")
            time.sleep(2)
            print("Как только тревоги стали реже, мы смогли наконец выдохнуть с облегчением.")
            time.sleep(1)
            print(
                "Вокруг по-прежнему остаются разрушения, но теперь перед вами стоит новая задача — восстановление вашего дома и жизни.")
            time.sleep(2)
            print("Эти 20 дней навсегда изменят ваше восприятие мира. Вы поняли ценность семьи, дома и мирной жизни.")
            time.sleep(1)
            print("Ваше следующее лето будет уже другим. Но сейчас, главное — вы вместе и выжили. И это новое начало.")

    # Пример использования
manager = GameManager()
