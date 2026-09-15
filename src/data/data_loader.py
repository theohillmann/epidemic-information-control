import csv
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    time: int
    person_i: int
    person_j: int
    person_status_i: str
    person_status_j: str


def data_loader(data_path: str):
    with open(data_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for record in reader:
            yield Event(
                time=int(record["t"]),
                person_i=int(record["i"]),
                person_j=int(record["j"]),
                person_status_i=record["Si"],
                person_status_j=record["Sj"],
            )
