import os

from src.config import DATA_DIR
from data import data_loader, DatasetMetadata


LYON_PATH = os.path.join(DATA_DIR, "lyon", "detailed_list_of_contacts_Hospital.csv")
lyon_dataset_metadata = DatasetMetadata(
    time_unit="seconds",
    time_resolution=20,
    time_origin="2010-06-01 13:00:00",
)

events = data_loader(LYON_PATH)

for time in events.keys():
    print(f"Time: {time}")
    for event in events[time]:
        print(f"  Event: {event}")
