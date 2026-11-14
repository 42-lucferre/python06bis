import abc
from .entities import Creature, Flameling, Pyrodon, Shiftling, Morphagon


class CreatureFactory(abc.ABC):
    @abc.abstractmethod
    def create_base(self) -> Creature:
        ...

    @abc.abstractmethod
    def create_evolved(self) -> Creature:
        ...


class FlameFactory(CreatureFactory):
    def create_base(self) -> Flameling:
        return Flameling()

    def create_evolved(self) -> Pyrodon:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Shiftling:
        return Shiftling()

    def create_evolved(self) -> Morphagon:
        return Morphagon()
