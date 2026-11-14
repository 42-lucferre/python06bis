#!/usr/bin/env python3

import ex3
import typing

if __name__ == "__main__":
    factory = ex3.TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing Creature with transform capability")

    entities: list[typing.Any] = [base, evolved]

    for i, entity in enumerate(entities):
        if i == 0:
            print(" base:")
        print(entity.describe())
        print(entity.attack())
        print(entity.transform())
        print(entity.attack())
        print(entity.revert())
        if i == 0:
            print(" evolved:")
