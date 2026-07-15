from abc import ABC, abstractmethod
from typing import Any, Optional, List, Union


class Validator(ABC):
    """Базовий абстрактний клас для дескрипторів валідації."""

    def __init__(self, protected_name: str) -> None:
        self.protected_name = f"_{protected_name}"

    def __set_name__(self, owner: type, name: str) -> None:
        """Метод для ініціалізації імені дескриптора."""
        self.protected_name = f"_{name}"

    def __set__(self, obj: object, value: Any) -> None:
        """Встановлює значення атрибута без валідації."""
        setattr(obj, self.protected_name, value)

    def __get__(self, obj: object, objtype: Optional[type] = None) -> Any:
        """Повертає значення атрибута."""
        return getattr(obj, self.protected_name)

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Абстрактний метод для валідації значення."""
        pass


class Number(Validator):
    """Descriptor for validating integer values within a range."""

    def __init__(
        self,
        protected_name: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ) -> None:
        super().__init__(protected_name)
        self.min_value = min_value
        self.max_value = max_value

    def __set__(self, obj: object, value: Union[int, float]) -> None:
        """Встановлює значення після валідації."""
        self.validate(value)
        super().__set__(obj, value)

    def validate(self, value: Any) -> None:
        """Перевіряє, чи значення є числом і потрапляє в діапазон."""
        if not isinstance(value, (int, float)):
            raise TypeError("Quantity should be integer.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(
                f"{self.protected_name[1:]} must be >= {self.min_value}"
            )
        if self.max_value is not None and value > self.max_value:
            raise ValueError(
                f"{self.protected_name[1:]} must be <= {self.max_value}"
            )


class OneOf(Validator):
    """Дескриптор для валідації значень з фіксованого списку."""

    def __init__(self, protected_name: str, options: List[Any]) -> None:
        super().__init__(protected_name)
        self.options = options

    def __set__(self, obj: object, value: Any) -> None:
        """Встановлює значення після валідації."""
        self.validate(value)
        super().__set__(obj, value)

    def validate(self, value: Any) -> None:
        """Перевіряє, чи значення міститься в списку допустимих значень."""
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {tuple(self.options)}."
            )


class BurgerRecipe:
    """Class representing a burger recipe with validated ingredients."""

    buns = Number("buns", min_value=2, max_value=3)
    cheese = Number("cheese", min_value=0, max_value=2)
    tomatoes = Number("tomatoes", min_value=0, max_value=3)
    cutlets = Number("cutlets", min_value=1, max_value=3)
    eggs = Number("eggs", min_value=0, max_value=2)
    sauce = OneOf("sauce", options=["ketchup", "mayo", "burger"])

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str,
    ) -> None:
        """Initialize a burger recipe with validated ingredients."""
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
