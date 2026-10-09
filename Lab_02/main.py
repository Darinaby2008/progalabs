from parrot import Parrot
from turtle import Turtle
from person import Person

def main():
    # Создаем питомцев
    kesha = Parrot("Kesha", 4)
    zavala = Turtle("Zavala", 4)

    kesha.happy_birthday() # Кеше исполнилось 5 лет

    # Создаем людей
    jack = Person("Jack", kesha)
    john = Person("John")

    # Выводим информацию
    jack.get_pet_info()
    john.get_pet_info()

    # Джон заводит черепаху
    john.set_pet(zavala)
    john.get_pet_info()

if __name__ == "__main__":
    main()