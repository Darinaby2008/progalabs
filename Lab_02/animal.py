from pet import Pet

class Animal(Pet):
    """
    Абстрактный класс. Мы не можем создать просто 'Animal', 
    только его наследников (Parrot, Turtle).
    """
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    def happy_birthday(self):
        self._age += 1

    def get_name(self) -> str:
        return self._name

    def get_age(self) -> int:
        return self._age
