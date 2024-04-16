import random
import time


class Character:
    def __init__(self,manager, name,max_health):
        self.name = name
        self.health = max_health//2  # начальное состояние здоровья
        self.max_health=max_health
        self.dead=False
        self.manager=manager
        self.location='В доме'# Подвал, Улица
    def reset_actions(self):
        if self.location=='ищет ресурсы':
            self.location='В доме'
    def can_act(self):
        return self.health>=2 and not self.dead and not self.in_basement()
    def take_damage(self,damage):
        if self.dead:
            return
        self.health-=damage
        txt=f'{self.name} получил {damage} урона'
        if self.health<0:
            self.dead=True
            self.health=-1
            txt+=' и погиб'
        else:
            txt+=f', осталось {self.health}hp / {self.max_health}hp'
        print(txt)

    def feed(self, food_storage):
        if self.health >= self.max_health or self.dead:
            return False

        food_storage.status()  # Показать текущий статус холодильника и доступную еду
        food_choice = input("Выберите продукт для употребления (введите номер): ")
        try:
            food_index = int(food_choice)-1
            if food_index >= 0 and food_index < len(food_storage.food):
                food = food_storage.food.pop(food_index)
                self.health = min(self.health + food.amount, self.max_health)
                print(f'{self.name} съел {food.name}, получено {food.amount} HP.')
                return True
            else:
                print("Неверный выбор.")
                return False
        except ValueError:
            print("Некорректный ввод.")
            return False
    def in_basement(self):
        return self.location=='подвал'
    def hide_in_basement(self):
        if self.location== 'подвал':
            return False
        self.location='подвал'
        return True

    def return_from_basement(self):
        if self.location == 'подвал':
            self.location = 'В доме'
        else:
            return False
        return True

    def gather_resources(self, food_storage, resource_type='еда'):
        if self.can_act():
            self.location = 'ищет ресурсы'
            # Генерация ресурсов
            if resource_type == 'еда':
                from food import Food
                resource_to_gather = Food.generate(self.manager)
            else:
                from food import Fuel
                resource_to_gather = Fuel.generate(self.manager)
            food_storage.add_food(resource_to_gather)

            health_consumed = random.randint(0, 2)
            event_chance = random.random()  # Шанс события

            txt = f'{self.name} нашел {resource_to_gather}'
            if health_consumed:
                statuses = [
                    'подскользнулся и упал', 'замерз из-за холода', 'устал от долгого поиска',
                    'столкнулся с разбойниками', 'нашел опасные животные', 'потерял ориентацию',
                    'нашел сломанную технику', 'заблудился в лесу', 'нашел заброшенный дом',
                    'встретил других выживших', 'испугался странных звуков', 'обнаружил старый склад',
                    'столкнулся с беженцами', 'обнаружил контрольно-пропускной пункт', 'нашел редкие растения',
                    'видел диких животных', 'нашел ручей с чистой водой', 'столкнулся с охраняемой территорией',
                    'нашел старые военные запасы', 'увидел отлетающий вертолет'
                ]
                status = random.choice(statuses)
                txt += f'. Но {status}'

            # Логика случайных встреч и квестов
            if event_chance < 0.2:  # Например, 20% шанс встречи
                txt += self.encounter_scenario()

            print(txt)
            if health_consumed:
                self.take_damage(health_consumed)
            return True
        return False

    def encounter_scenario(self):
        encounters = [
            ("встретил торговца", "Поторговаться или продолжить путь? [торг/путь]"),
            ("нашел раненого животного", "Помочь животному или оставить его? [помочь/оставить]"),
            ("столкнулся с бродягой", "Поделиться едой или проигнорировать? [поделиться/игнор]")
        ]
        encounter, question = random.choice(encounters)
        response = input(f"{self.name} {encounter}. {question} ")

        # Решения игрока
        if encounter == "встретил торговца":
            return self.trade_with_merchant(response)
        elif encounter == "нашел раненого животного":
            return self.help_animal(response)
        elif encounter == "столкнулся с бродягой":
            return self.deal_with_beggar(response)
        return " и продолжил путь."

    def trade_with_merchant(self, response):
        if response.lower() == "торг":
            # Логика торговли
            from food import Food
            res = Food.generate(self.manager)
            self.manager.food_storage.add_food(res)
            return f", торговался и получил выгодное предложение: {res}"
        return ", не стал торговаться."

    def help_animal(self, response):
        if response.lower() == "помочь":
            # Логика помощи животному
            from food import Food
            res = Food.generate(self.manager)
            self.manager.food_storage.add_food(res)
            return f", помог животному, и оно принесло {res}"
        return ", оставил животное в покое."

    def deal_with_beggar(self, response):
        if response.lower() == "поделиться":
            # Логика взаимодействия с бродягой
            return ", поделился едой и получил благословение."
        return ", проигнорировал бродягу."

    def __str__(self):
        return f"{self.name}: Состояние = {self.health}/{self.max_health},  {' (мертв)' if self.dead else self.location}"
