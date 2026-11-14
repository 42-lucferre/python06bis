#!/usr/bin/env python3

import ex3


def activate_factory(factory: ex3.CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    print()


def battle_factory(factory0: ex3.CreatureFactory,
                   factory1: ex3.CreatureFactory) -> None:
    print("Testing battle")
    base0 = factory0.create_base()
    base1 = factory1.create_base()

    print(base0.describe())
    print(" vs.")
    print(base1.describe())
    print(" fight!")
    print(base0.attack())
    print(base1.attack())


if __name__ == "__main__":
    factory_0 = ex3.FlameFactory()
    factory_1 = ex3.TransformCreatureFactory()

    activate_factory(factory_0)
    activate_factory(factory_1)

    battle_factory(factory_0, factory_1)
