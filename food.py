import random


all_food=[]
class Fuel:
    def __init__(self,manager,name,amount):
        self.amount=amount
        self.name=name
        self.manager=manager
    @classmethod
    def generate(cls,manager):
        names = ['Бензин', 'Дрова']
        amount = random.randint(1, 3)
        return cls(manager,random.choice(names), amount)

    def __str__(self):
        txt = f"Топливо {self.name} +{self.amount}"
        return txt
class Food:
    def __init__(self,manager, name,expire_in_days=3,amount=1):

        self.name=name
        self.expire_in_days=expire_in_days
        self.amount=amount
        self.manager=manager
        self.created_at_day=manager.current_day
        self.expire_rate=1/self.expire_in_days
        self.expire_rate_not_in_fridge= self.expire_rate * 5
        self.expire_progress=0

        all_food.append(self)
        self.storage=None
        self.is_expired=False
    def new_day(self):
        expire_rate=self.expire_rate if self.storage and self.storage.is_working else self.expire_rate_not_in_fridge
        self.expire_progress+=expire_rate
        if self.expire_progress>=1:
            self.amount=0
            self.is_expired=True
            self.expire_progress=1

    @classmethod
    def generate(self,manager)-> 'Food':
        names = ['Помидор', 'Яблоко', 'Огурец','Свинина','Курятина','Макароны']
        amount = random.randint(1, 5)
        expire_in_days = random.randint(2, 14)
        return Food(manager,random.choice(names), amount=amount, expire_in_days=expire_in_days)

    def __str__(self):
        txt= f"Еда {self.name} +{self.amount}"
        if self.expire_progress>0:
             txt+=f": {self.expire_progress*100:.1f}% испорченность"
        return txt
