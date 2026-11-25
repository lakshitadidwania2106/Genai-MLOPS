
import json
import os
from app.connectors.ollama_connector import OllamaConnector

connector = OllamaConnector("llama3.2:1b")

prompt = """
Explain what machine learning is.
Give a simple definition and one practical example.
"""

os.makedirs("results", exist_ok=True)

results = []

# A: Change temperature, seed fixed
temperatures = [0.0, 0.2, 0.5, 0.8]

for temperature in temperatures:

    for run in range(5):

        result = connector.generate(
            prompt,
            temperature=temperature,
            seed=42
        )

        result["experiment"] = "temperature"
        result["run"] = run + 1

        results.append(result)

        print(
            "Temperature:", temperature,
            "| Run:", run + 1,
            "| Output:", result["output"][:80]
        )


#B: Change seed, temperature fixed
seeds = [42, 43, 44, 45, 46]

for seed in seeds:

    for run in range(5):

        result = connector.generate(
            prompt,
            temperature=0.3,
            seed=seed
        )

        result["experiment"] = "seed"
        result["run"] = run + 1

        results.append(result)

        print(
            "Seed:", seed,
            "| Run:", run + 1,
            "| Output:", result["output"][:80]
        )


with open(
    "results/day8_controlled_runs.jsonl",
    "w"
) as file:

    for result in results:
        file.write(json.dumps(result) + "\n")

print("\nExperiment completed!")
print("Total runs:", len(results))
