#!/usr/bin/env python3

import ex4
import ex3
import typing


def battle_tournament(opp: list[tuple[ex3.CreatureFactory,
                                      ex4.strategy.BattleStrategy]]) -> None:
    opp_print: list[typing.Any] = []
    opp_base: list[typing.Any] = []
    for item in opp:
        entity = item[0].create_base()
        strategy = item[1]
        opp_print.append(tuple([entity.name, strategy.name]))
        opp_base.append(tuple([entity, strategy]))
    print(opp_print)

    print("*** Tournament ***")
    print(f"{len(opp)} opponents involved")

    print("\n* Battle *")
    for i in range(len(opp)):
        for j in range(i + 1, len(opp)):
            print(opp_base[i][0].describe())
            print(" vs.")
            print(opp_base[j][0].describe())
            print(" now fight!")
            try:
                opp_base[i][1].act(opp_base[i][0])
                opp_base[j][1].act(opp_base[j][0])
            except ex4.strategy.StrategyError as e:
                print(f"Battle error, aborting tournament: {e}")


if __name__ == "__main__":
    print("Tournament 0 (basic)")

    factory0 = ex3.FlameFactory()
    factory1 = ex3.TransformCreatureFactory()

    normal = ex4.strategy.NormalStrategy()
    aggressive = ex4.strategy.AggressiveStrategy()

    tournament0: typing.Any = [(factory0, normal), (factory1, aggressive)]
    battle_tournament(tournament0)

    print("\nTournament 1 (error)")
    tournament1: typing.Any = [(factory1, aggressive), (factory0, aggressive)]
    battle_tournament(tournament1)
