import os

from src.config import DATA_DIR
from data.lyon_loader import data_loader

LYON_PATH = os.path.join(DATA_DIR, "lyon", "detailed_list_of_contacts_Hospital.csv")


events = data_loader(LYON_PATH)

for time in events.keys():
    print(f"Time: {time}")
    for event in events[time]:
        print(f"  Event: {event}")
