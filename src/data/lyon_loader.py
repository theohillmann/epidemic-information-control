import os
import pandas as pd

from src.config import DATA_DIR, PROJECT_ROOT

LYON_PATH = os.path.join(DATA_DIR, "lyon", "detailed_list_of_contacts_Hospital.csv")

df = pd.read_csv(LYON_PATH, sep="\t")

print(df['t'])