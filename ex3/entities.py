import abc
import typing


class Creature(abc.ABC):
    def __init__(self, name: str, type_: str) -> None:
        self.name = name
        self.type_ = type_

    @abc.abstractmethod
    def attack() -> None:
        ...

    