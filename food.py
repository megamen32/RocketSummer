import random


all_food=[]
class Fuel:
    def __init__(self,manager,name,amount):
        self.amount=amount
        self.name=name
        self.manager=manager

    @classmethod
    def generate(cls, manager):
        names = [
            'Бензин', 'Дрова', 'Уголь', 'Газ', 'Биотопливо', 'Керосин', 'Спирт', 'Торф',
            'Пеллеты', 'Мазут', 'Водород', 'Этанол', 'Метан', 'Пропан', 'Бутан',
            'Жидкое топливо', 'Сжатый природный газ', 'Сжиженный нефтяной газ', 'Дизельное топливо',
            'Авиационный керосин'
        ]
        amount = random.randint(1, 3)
        return cls(manager, random.choice(names), amount)

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
        expire_rate = self.cur_expire_rate()
        self.expire_progress+=expire_rate
        if self.expire_progress>=1:
            self.amount=0
            self.is_expired=True
            self.expire_progress=1

    def cur_expire_rate(self):
        expire_rate = self.expire_rate if self.storage and self.storage.is_working() else self.expire_rate_not_in_fridge
        return expire_rate

    @classmethod
    def generate(cls, manager):
        names = [
            'Помидор', 'Яблоко', 'Огурец', 'Свинина', 'Курятина', 'Макароны', 'Картофель',
            'Морковь', 'Капуста', 'Лук', 'Чеснок', 'Банан', 'Груша', 'Слива', 'Вишня',
            'Говядина', 'Рыба', 'Яйца', 'Молоко', 'Сыр'
        ]
        amount = random.randint(1, 5)
        expire_in_days = random.randint(2, 14)
        return cls(manager, random.choice(names), amount, expire_in_days)

    def __str__(self):
        txt= f"Еда {self.name} +{self.amount}"

        txt+=f": испортиться через {(1-self.expire_progress)/self.cur_expire_rate():.1f} дней"
        return txt
