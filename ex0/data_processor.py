#!/usr/bin/env python3

import typing, abc


class DataProcessor(abc.ABC):

    def __init__(self) -> None:
        self.counter: int = 0
        self.data_list: list[typing.Any] = []

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        self.counter += 1
        return (self.counter, self.data_list.pop(0))


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        return False

    def ingest(self, data: typing.Any) -> None:
        try:
            self.validate(data)
        except Exception:
            raise Exception("Got exception: improper numeric data")

        for number in [data]:
            self.data_list.append(number)

# class TextProcessor(DataProcessor):



# class LogProcessor(DataProcessor):


if __name__ == "__main__":
    numeros = NumericProcessor()
    numeros.ingest(10)
    # numeros.ingest(20)
    out1 = numeros.output()
    print(f"Numeric value: {out1[0]}: {out1[1]}")
