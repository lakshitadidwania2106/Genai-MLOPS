
import json
import os

from app.connectors.ollama_connector import OllamaConnector

connector = OllamaConnector("llama3.2:1b")

prompt = """
Invent a fictional creature that has never existed.
Describe its appearance, habitat, behaviour,
and one unusual ability.
Be imaginative and specific.
"""

results = []

os.makedirs("results", exist_ok=True)

# Experiment A: Change top-k only
for top_k in [1, 5, 20, 100]:

    for run in range(5):

        result = connector.generate(
            prompt,
            temperature=0.8,
            seed=42,
            top_p=1.0,
            top_k=top_k
        )

        result["experiment"] = "top_k"
        result["run"] = run + 1

        results.append(result)

        print(
            "Top-k:", top_k,
            "| Run:", run + 1
        )


# Experiment B: Change top-p only
for top_p in [0.1, 0.5, 0.9]:

    for run in range(5):

        result = connector.generate(
            prompt,
            temperature=0.8,
            seed=42,
            top_p=top_p,
            top_k=100
        )

        result["experiment"] = "top_p"
        result["run"] = run + 1

        results.append(result)

        print(
            "Top-p:", top_p,
            "| Run:", run + 1
        )


with open(
    "results/day9_decoding_runs.jsonl",
    "w"
) as file:

    for result in results:
        file.write(json.dumps(result) + "\n")

print("\nExperiment completed!")
print("Total calls:", len(results))
