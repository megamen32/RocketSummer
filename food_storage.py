import random
from typing import List

from food import Food, all_food, Fuel


class FoodStorage:
    def __init__(self,manager,name='Холодильник',capacity=10):
        self.name=name
        self.manager=manager
        self.capacity = capacity
        self.food:List[Food]=[Food.generate(self.manager) for _ in range(random.randint(2,5))] if name =='Холодильник' else [Fuel.generate(self.manager) for _ in range(1)]
        self.food_count = lambda :len(self.food)
        self.food_amount = lambda :sum([food.amount for food in self.food if food.amount>0])
        self._hp=1
        self._electricity=lambda :self.manager.house.is_electricty()
        self.is_working=lambda :self._hp>0 and self._electricity()# Will turn of by electicity


    def add_food(self, food: Food):
        if self.food_count() < self.capacity:
            food.storage=self
            self.food.append(food)
            return True
        return False
    def repair(self):
        if self._hp>0: return False
        self._hp=1
        print(f'{self.name} починен')
        return True

    def consume_food(self):
        if self.food_count() > 0:
            food=self.food.pop()
            all_food.remove(food)
            food.storage=None
            return food
        return None


    def __str__(self):
        status = 'в порядке'
        if self._hp ==0:
            status='сломан(нужен ремонт)'
        if not self._electricity:
            status+='нет электричества(нужен генератор)'
        return f"{self.name} {status} Емкость: {self.food_count()}/{self.capacity}"
    def status(self):
        print(f"Содержимое {self.name}:")
        for index, food in enumerate((self.food), 1):
            print(f"{index}. {food}")
        print(self.__str__())
    def clear_trash(self):
        self.food=[food for food in self.food if not food.is_expired]
        print('Все протухшие продукты были выкинуты')
        return True
