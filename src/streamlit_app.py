import streamlit as st
from src.epidemic.main import Epidemic

if __name__ == "__main__":

    with st.sidebar:
        st.title("Epidemic Simulation")
        cycles = st.slider("Number of cycles", min_value=1, max_value=20, value=6)
        seed = st.number_input("Seed", value=95)
        incubation_period = st.number_input("Incubation Period (seconds)", value=432000)
        infectious_period = st.number_input("Infectious Period (seconds)", value=604800)
        transmission_probability = st.number_input(
            "Transmission Probability", value=0.005, step=0.001
        )
        snapshot_interval_seconds = st.number_input(
            "Snapshot Interval (seconds)", value=900
        )

    epidemic = Epidemic(
        seed=seed,
        incubation_period=incubation_period,
        infectious_period=infectious_period,
        transmission_probability=transmission_probability,
        snapshot_interval_seconds=snapshot_interval_seconds,
    )
    result = epidemic.run(cycles=cycles)

    if st.button("Run Simulation"):
        result = epidemic.run(cycles=cycles)
        st.write("Simulation Results:")
        st.write(result)
