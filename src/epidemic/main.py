import os
import numpy as np
from enum import Enum
from datetime import timedelta
from collections import Counter
from dataclasses import dataclass

from src.config import DATA_DIR
from src.data import data_loader, DatasetMetadata


LYON_PATH = os.path.join(DATA_DIR, "lyon", "detailed_list_of_contacts_Hospital.csv")
lyon_dataset_metadata = DatasetMetadata(
    time_unit="seconds",
    time_resolution=20,
    time_origin="2010-12-06 13:00:00",
)


class DiseaseState(Enum):
    SUSCEPTIBLE = "S"
    EXPOSED = "E"
    INFECTIOUS = "I"
    RECOVERED = "R"


@dataclass
class HealthState:
    state: DiseaseState
    entered_at: float

    def transition_to(self, new_state, current_time):
        self.state = new_state
        self.entered_at = current_time


class Epidemic:

    def __init__(
        self,
        seed=95,
        incubation_period=432000,
        infectious_period=604800,
        transmission_probability=0.005,
        snapshot_interval_seconds=900,
    ):
        """
        :param seed: Random seed for reproducibility. Defaults to 95.
        :param incubation_period: Time an individual spends in the exposed state,
            in seconds. Defaults to 5 days (432,000 seconds).
        :param infectious_period: Time an individual spends in the infectious state,
            in seconds. Defaults to 7 days (604,800 seconds).
        :param transmission_probability: Probability of transmission during a contact.
            Defaults to 0.005 (0.5%).
        :param snapshot_interval_seconds: Interval between snapshots, in seconds.
            Defaults to 15 minutes (900 seconds).
        """
        self.SEED = seed
        self.rng = np.random.default_rng(self.SEED)

        self.incubation_period = incubation_period
        self.infectious_period = infectious_period
        self.transmission_probability = transmission_probability

        self.snapshot_interval_seconds = snapshot_interval_seconds

        self.people = set()
        self.state = dict()
        self.history = []

        self.__define_people()
        self.__set_states()

    def __define_people(self):
        for event in data_loader(LYON_PATH):
            self.people.add(event.person_i)
            self.people.add(event.person_j)

    def __set_states(self):
        patient_zero = self.rng.choice(sorted(self.people))
        self.state = {
            person: HealthState(state=DiseaseState.SUSCEPTIBLE, entered_at=0)
            for person in self.people
        }
        self.state[patient_zero] = HealthState(
            state=DiseaseState.INFECTIOUS, entered_at=0
        )
        print(f"Patient zero is person {patient_zero}")

    def run(self, cycles=1):
        events = list(data_loader(LYON_PATH))

        start_time = events[0].time
        end_time = events[-1].time
        recording_duration = end_time - start_time

        for cycle in range(cycles):
            next_snapshot = 0

            for event in events:
                simulation_time = event.time - start_time + cycle * recording_duration

                self.update_states(simulation_time)
                self.process_contact(event.person_i, event.person_j, simulation_time)

                if simulation_time >= next_snapshot:
                    self.snapshot(simulation_time)
                    next_snapshot += self.snapshot_interval_seconds

        return self.get_state()

    def process_contact(self, person_i, person_j, event_time):
        state_i = self.state[person_i].state
        state_j = self.state[person_j].state

        if {state_i, state_j} != {DiseaseState.INFECTIOUS, DiseaseState.SUSCEPTIBLE}:
            return
        susceptible = person_i if state_i == DiseaseState.SUSCEPTIBLE else person_j

        if self.rng.random() < self.transmission_probability:
            self.state[susceptible] = HealthState(
                state=DiseaseState.EXPOSED, entered_at=event_time
            )

    def update_states(self, current_time):
        for health_state in self.state.values():

            time_in_state = current_time - health_state.entered_at

            if (
                health_state.state == DiseaseState.EXPOSED
                and time_in_state >= self.incubation_period
            ):
                health_state.transition_to(DiseaseState.INFECTIOUS, current_time)

            elif (
                health_state.state == DiseaseState.INFECTIOUS
                and time_in_state >= self.infectious_period
            ):
                health_state.transition_to(DiseaseState.RECOVERED, current_time)

    def snapshot(self, simulation_time):
        counts = Counter(health_state.state for health_state in self.state.values())
        self.history.append(
            {
                "time": simulation_time,
                "S": counts[DiseaseState.SUSCEPTIBLE],
                "E": counts[DiseaseState.EXPOSED],
                "I": counts[DiseaseState.INFECTIOUS],
                "R": counts[DiseaseState.RECOVERED],
            }
        )

    def get_current_time(self, simulation_time):
        return lyon_dataset_metadata.time_origin + timedelta(seconds=simulation_time)

    def get_state(self):
        counts = Counter(health_state.state for health_state in self.state.values())

        return {
            "Susceptible": counts[DiseaseState.SUSCEPTIBLE],
            "Exposed": counts[DiseaseState.EXPOSED],
            "Infectious": counts[DiseaseState.INFECTIOUS],
            "Recovered": counts[DiseaseState.RECOVERED],
        }


if __name__ == "__main__":
    epidemic = Epidemic()
    res = epidemic.run(cycles=6)
    print(res)
