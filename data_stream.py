#!/usr/bin/env python3

import typing
import abc


class DataProcessor(abc.ABC):

    def __init__(self) -> None:
        self.counter: int = -1
        self.data_list: list[str] = []

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if self.data_list:
            self.counter += 1
            return (self.counter, self.data_list.pop(0))
        else:
            raise Exception("Can't output from empty list")


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            if all(isinstance(item, (int, float)) for item in data):
                return True
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        if not isinstance(data, list):
            data = [data]
        for number in data:
            self.data_list.append(str(number))


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            if all(isinstance(item, str) for item in data):
                return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")

        if not isinstance(data, list):
            data = [data]
        for item in data:
            self.data_list.append(item)


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        def is_str_dict(dct: dict[typing.Any, typing.Any]) -> bool:
            if all(isinstance(k, str) and isinstance(v, str)
                   for k, v in dct.items()):
                return True
            return False

        if isinstance(data, dict):
            return is_str_dict(data)
        if isinstance(data, list):
            if all(isinstance(item, dict) and is_str_dict(item)
                   for item in data):
                return True
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise Exception("Improper dict data")

        if not isinstance(data, list):
            data = [data]
        for item in data:
            self.data_list.append(list(item.values())[0] + ": "
                                  + list(item.values())[1])


class DataStream():
    def __init__(self) -> None:
        self.num_counter = 0
        self.text_counter = 0
        self.log_counter = 0

    def register_processor(self, proc: DataProcessor) -> None:
        proc.ingest()

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            if NumericProcessor.validate(item):
                item = NumericProcessor()
                self.register_processor(item)
                self.num_counter += 1

    def print_processors_stats(self) -> None:
        if not all([self.num_counter, self.text_counter, self.log_counter]):
            print("No processor found, no data")
            return 
        print(f"Numeric Processor: total {} items processed, "
              f"remaining {} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    nodata = DataStream()
    print("== DataStream statistics ==\n")
    nodata.print_processors_stats()
    print(f" Trying to validate input '42': {numbers.validate(42)}")
    print(f" Trying to validate input 'Hello': {numbers.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numbers.ingest("foo")
    except Exception as e:
        print(f" Got exception: {e}")
    print(" Processing data: [1, 2, 3, 4, 5]")
    numbers.ingest([1, 2, 3, 4, 5])
    print(" Extracting 3 values...")
    for _ in range(3):
        try:
            out = numbers.output()
            print(f" Numeric value {out[0]}: {out[1]}")
        except Exception as e:
            print(f" Got exception: {e}")

    texts = TextProcessor()
    print("\nTesting Text Processor...")
    print(f" Trying to validate input '42': {texts.validate(42)}")
    print(" Processing data: ['Hello', 'Nexus', 'World']")
    try:
        texts.ingest(['Hello', 'Nexus', 'World'])
        print(" Extracting 1 value...")
        out = texts.output()
        print(f" Text value {out[0]}: {out[1]}")
    except Exception as e:
        print(f" Got exception: {e}")

    logs = LogProcessor()
    print("\nTesting Log Processor...")
    print(f" Trying to validate input 'Hello': {logs.validate('Hello')}")
    log_list = [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
                {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
    print(f" Processing data: {log_list}")
    logs.ingest(log_list)
    print(" Extracting 2 values...")
    try:
        for _ in range(2):
            out = logs.output()
            print(f" Log entry {out[0]}: {out[1]}")
    except Exception as e:
        print(f" Got exception: {e}")
