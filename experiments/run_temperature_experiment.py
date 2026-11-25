
import json
from datetime import datetime, timezone
from pathlib import Path
from app.connectors.ollama_connector import OllamaConnector

MODEL_NAME = "llama3.2:1b" #the different configuration

TEMPERATURES = [0.0, 0.3, 0.7]

SEEDS = [42, 43, 44, 45, 46]

PROMPT = """
Explain what machine learning is
in exactly three simple sentences.
"""

connector = OllamaConnector(MODEL_NAME)

all_results = []

print("GENAI TEMPERATURE EXPERIMENT")
print("=" * 40)

for temperature in TEMPERATURES: #for different temps

    print(f"\nTesting temperature: {temperature}")

    for seed in SEEDS:

        print(f"Running with seed {seed}...")

        result = connector.generate(
            prompt=PROMPT,
            temperature=temperature,
            seed=seed
        )

        result["seed"] = seed
        result["experiment_type"] = "temperature_sensitivity"
        result["timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

        all_results.append(result)

        print(result["output"])
        print("-" * 30)
Path("results").mkdir(exist_ok=True)

output_file = Path(
    "results/day4_temperature_runs.jsonl"
)

with output_file.open("w", encoding="utf-8") as file:

    for result in all_results:
        file.write(json.dumps(result) + "\n")

print("\nExperiment completed!")
print("Total runs:", len(all_results))
print("Saved to:", output_file)
