from abc import ABC, abstractmethod
import typing


class Validator(ABC):
    """Base validator class for descriptors."""

    protected_name: str

    def __set_name__(self, owner: type, name: str) -> None:
        """Set the protected name for the attribute."""
        self.protected_name = f"_{name}"

    def __get__(self, obj: typing.Any, obj_type: type = None) -> typing.Any:
        """Get the attribute value from the object."""
        return getattr(obj, self.protected_name)

    def __set__(self, obj: typing.Any, value: typing.Any) -> None:
        """Set the attribute value after validation."""
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: typing.Any) -> None:
        """Validate the value."""
        pass


class Number(Validator):
    """Validator for numeric values within a range."""
    def __init__(self, min_value: int, max_value: int) -> None:
        """Initialize the Number validator with min and max values."""
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: typing.Any) -> None:
        """Validate that the value is within the specified range."""
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    """Validator for values from a predefined set of options."""
    def __init__(self, *options: typing.Any) -> None:
        """Initialize with allowed options."""
        self.options = options

    def validate(self, value: typing.Any) -> None:
        """Validate that the value is one of the allowed options."""
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    """Class representing a burger recipe with validated ingredients."""

    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf("ketchup", "mayo", "burger")

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
