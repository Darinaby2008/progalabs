from abc import ABC, abstractmethod

class Pet(ABC):
    """
    Это интерфейс (контракт). Все, кто называют себя Pet, 
    ОБЯЗАНЫ реализовать эти методы.
    """
    @abstractmethod
    def express(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_age(self):
        pass

    @abstractmethod
    def get_age_in_human_years(self):
        pass