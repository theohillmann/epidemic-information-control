import pandas as pd
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    time: int
    person_i: str
    person_j: str
    person_status_i: str
    person_status_j: str


def data_loader(data_path: str):
    df = pd.read_csv(data_path, sep="\t")

    for record in df.to_dict(orient="records"):
        yield Event(
            time=record["t"],
            person_i=record["i"],
            person_j=record["j"],
            person_status_i=record["Si"],
            person_status_j=record["Sj"],
        )
