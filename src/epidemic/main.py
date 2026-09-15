import os
from datetime import timedelta

from src.config import DATA_DIR
from src.data import data_loader, DatasetMetadata


LYON_PATH = os.path.join(DATA_DIR, "lyon", "detailed_list_of_contacts_Hospital.csv")
lyon_dataset_metadata = DatasetMetadata(
    time_unit="seconds",
    time_resolution=20,
    time_origin="2010-12-06 13:00:00",
)

cycles = 3
correction_time = 0
for repetitions in range(cycles):
    events = data_loader(
        LYON_PATH,
    )

    for index, event in enumerate(events):
        date = lyon_dataset_metadata.time_origin + timedelta(
            seconds=event.time + correction_time
        )
        print(date)

    correction_time += event.time
