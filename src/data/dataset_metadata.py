from typing import Union
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DatasetMetadata:
    time_unit: str
    time_resolution: int
    time_origin: Union[str, datetime]

    def __post_init__(self):
        self.time_origin = datetime.strptime(self.time_origin, "%Y-%m-%d %H:%M:%S")
