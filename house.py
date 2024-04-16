import random

class Generator():
    def __init__(self,manager):
        self.is_turned_on=False
        self.is_malfunction=False
        self.current_fuel=None
        self.manager=manager
    def is_turned_on_and_working(self):
        return self.is_turned_on and not self.is_malfunction
    def turn_on(self):
        if self.is_turned_on:
            return False
        if self.is_malfunction:
            return False
        if not self.current_fuel:
            self.manager.fuel_storage.status()  # Показать текущий статус холодильника и доступную еду
            food_choice = input("Выберите топливо для сжигания (введите номер): ")
            try:
                food_index = int(food_choice) - 1
                if food_index >= 0 and food_index < len(self.manager.fuel_storage.food):
                    food = self.manager.fuel_storage.food.pop(food_index)
                    self.current_fuel=food
                    self.is_turned_on=True
                    print(f'Сегодня будет сожжено: {food.name}')
                    return True
                else:
                    print("Неверный выбор.")
                    return False
            except ValueError:
                print("Некорректный ввод.")
                return False
        else:
            self.is_turned_on = True
    def turn_off(self):
        if not self.is_turned_on or self.is_malfunction:
            return False
        self.is_turned_on=False
        print('Генератор выключен')

    def new_day(self):
        if self.current_fuel and self.is_turned_on:
            self.current_fuel.amount-=1
            print(f'Генератор сжигает {self.current_fuel.name}, осталось {self.current_fuel.amount} дней')
            if self.current_fuel.amount<=0:
                self.current_fuel=None
                self.is_turned_on=False

        
        
        
class House:
    def __init__(self,manager):
        self.durability = 100  # начальная прочность дома
        self.electricity_from_outside=True
        self.generator=Generator(manager)
        self.manager=manager
        self.is_electricty = lambda: self.electricity_from_outside or self.generator.is_turned_on_and_working()
        
        

    def bombard(self):
        self.durability -= random.randint(0,20)  # уменьшение прочности дома после обстрела
        if self.durability < 0:
            self.durability = 0

    def repair(self):
        if self.durability < 100:
            self.durability += 5  # ремонт дома
            if self.durability > 100:
                self.durability = 100
            print(f'Дом починен: {self.durability}%')
            return True
        return False

    def __str__(self):
        return f"Прочность дома: {self.durability}%,  Электричество {'в порядке' if self.electricity_from_outside else ('отлючено(включите генратор)' if not self.generator.is_turned_on_and_working() else 'от генератора')}, Генератор: {'включен'  if self.generator.is_turned_on else 'выключен'}\n{self.manager.food_storage}"
