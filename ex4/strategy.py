import abc
from ex3.entities import Creature, TransformCapability
import typing


class StrategyError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class BattleStrategy(abc.ABC):
    name: str

    @abc.abstractmethod
    def is_valid(self, entity: Creature) -> bool:
        ...

    @abc.abstractmethod
    def act(self, entity: Creature) -> None:
        ...


class NormalStrategy(BattleStrategy):
    def __init__(self) -> None:
        self.name: str = "Normal"

    def is_valid(self, entity: Creature) -> bool:
        return True

    def act(self, entity: Creature) -> None:
        if self.is_valid(entity):
            print(entity.attack())
        else:
            raise StrategyError(f"Invalid Creature {entity.name} for "
                                "this normal strategy")


class AggressiveStrategy(BattleStrategy):
    def __init__(self) -> None:
        self.name: str = "Aggressive"

    def is_valid(self, entity: Creature) -> bool:
        if isinstance(entity, TransformCapability):
            return True
        return False

    def act(self, entity: Creature) -> None:
        if self.is_valid(entity):
            casted = typing.cast(TransformCapability, entity)
            print(casted.transform())
            print(entity.attack())
            print(casted.revert())
        else:
            raise StrategyError(f"Invalid Creature '{entity.name}' for "
                                "this aggressive strategy")
