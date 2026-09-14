from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetMetadata:
    time_unit: str
    time_resolution: int
    time_origin: str
