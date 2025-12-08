from abc import ABCMeta, abstractmethod
from typing import TypeVar

from rest_framework.exceptions import ValidationError


UseCaseActionReturn = TypeVar('UseCaseActionReturn')


class AbstractUseCase(metaclass=ABCMeta):
    def __post_init__(self):
        self.errors = {}

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def action(self):
        pass

    def execute(self) -> UseCaseActionReturn:
        self.validate()
        self.check_errors()
        return self.action()

    def add_error(self, field: str, message: str) -> None:
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

    def check_errors(self) -> None:
        if self.errors:
            raise ValidationError(self.errors)
