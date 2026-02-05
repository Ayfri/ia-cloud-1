from dataclasses import dataclass

@dataclass
class Data:
    data: list[list[int]]
    processed: bool = False
