from src.epidemic.main import Epidemic


transmission_probabilities = [
    0.001,
]

for p in transmission_probabilities:
    attack_rates = []

    for seed in range(20):
        epidemic = Epidemic(
            seed=seed,
            transmission_probability=p,
        )

        result = epidemic.run(cycles=None)

        print(
            f"p={p:.4f} | " f"attack rate={result['attack_rate']:.2%} | " f"seed={seed}"
        )
