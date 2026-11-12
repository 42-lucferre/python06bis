#!/usr/bin/env python3

import typing
import abc


class DataProcessor(abc.ABC):

    def __init__(self, name) -> None:
        self.counter: int = 0
        self.data_list: list[str] = []
        self.name: str = name

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
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

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
    def __init__(self) -> None:
        super().__init__("Text Processor")

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
    def __init__(self) -> None:
        super().__init__("Log Processor")

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


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self.processors:
            self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            processed = 0
            for processor in self.processors:
                if processor.validate(item):
                    processor.ingest(item)
                    processed = 1
                    break
            if not processed:
                print("DataStream error - Can't process "
                      f"element in stream: {item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            total_count = proc.counter + len(proc.data_list)
            print(f"{proc.name}: total {total_count} items "
                  f"processed, remaining {len(proc.data_list)} on processor")

    def output_pipeline(self, nb: int, plugin: "ExportPlugin") -> None:
        for proc in self.processors:
            output_list = []
            for i in range(nb):
                if proc.data_list:
                    output_list.append(proc.output())
            plugin.process_output(output_list)


class ExportPlugin(typing.Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print(data)


class ExportPluginCSV:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        csv_list = []
        for item in data:
            csv_list.append(item[1])
        print(*csv_list, sep=",")


class ExportPluginJSON:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        data_dict = {}
        for item in data:
            data_dict[f"item_{item[0]}"] = item[1]
        print(data_dict)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors")
    ds_num_proc = NumericProcessor()
    ds.register_processor(ds_num_proc)
    ds_text_proc = TextProcessor()
    ds.register_processor(ds_text_proc)
    ds_log_proc = LogProcessor()
    ds.register_processor(ds_log_proc)

    batch = ['Hello world', [3.14, -1, 2.71],
             [{'log_level': 'WARNING', 'log_message': 'Telnet access! '
               'Use ssh instead'},
              {'log_level': 'INFO', 'log_message': 'User wil is connected'}],
             42, ['Hi', 'five']]
    print(f"\nSend first batch of data on stream: {batch}\n")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    csv = ExportPluginCSV()
    ds.output_pipeline(3, csv)
    # try:
    #     ds_num_proc.output()
    #     ds_num_proc.output()
    #     ds_num_proc.output()
    #     ds_text_proc.output()
    #     ds_text_proc.output()
    #     ds_log_proc.output()
    # except Exception as e:
    #     print(f"{e}")
    # ds.print_processors_stats()
