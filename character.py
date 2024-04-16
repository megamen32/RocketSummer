import random
import time


class Character:
    def __init__(self,manager, name):
        self.name = name
        self.health = 5  # начальное состояние здоровья
        self.max_health=10
        self.dead=False
        self.manager=manager
        self.location='В доме'# Подвал, Улица
    def reset_actions(self):
        if self.location=='ищет ресурсы':
            self.location='В доме'
    def can_act(self):
        return self.health>=2 and not self.dead and not self.in_basement()
    def take_damage(self,damage):
        self.health-=damage
        txt=f'{self.name} получил {damage} урона'
        if self.health<0:
            self.dead=True
            self.health=-1
            txt+='и погиб'
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

    def gather_food(self, food_storage,resource_type='еда'):
        if self.can_act():
            self.location='ищет ресурсы'
            if resource_type=='еда':
                from food import Food
                food_to_gather=Food.generate(self.manager)
                food_storage.add_food(food_to_gather)
            else:
                from food import Fuel
                food_to_gather = Fuel.generate(self.manager)
                food_storage.add_food(food_to_gather)

            health_consumed = random.randint(0, 2)

            txt = f'Нашел {food_to_gather}'
            if health_consumed:
                statuses=['упал', 'замерз' ,'устал' ,'напали разбойники']
                txt+=f'. Но {random.choice(statuses)}'
            print(txt)
            if health_consumed:
                time.sleep(1)
                self.take_damage(health_consumed)
            return True
        return False


    def __str__(self):
        return f"{self.name}: Состояние = {self.health}/{self.max_health},  {' (мертв)' if self.dead else self.location}"
