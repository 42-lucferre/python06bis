#!/usr/bin/env python3

import ex3


if __name__ == "__main__":
    factory = ex3.TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing Creature with transform capability")

    print(" base:")
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())

    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())
