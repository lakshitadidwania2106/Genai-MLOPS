
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.connectors.ollama_connector import OllamaConnector


#experiment configuration
MODEL_NAME = "llama3.2:1b"
TEMPERATURE = 0.0
SEED = 42
NUM_RUNS = 5 #it means model sends the prompt 5 times and records it
PROMPT_VERSION = "v1"

PROMPT = """
Explain what machine learning is
in exactly three simple sentences.
"""


# Create connector
connector = OllamaConnector(MODEL_NAME)

# Create experiment ID
experiment_id = str(uuid.uuid4())

# Store all responses
results = []

print("Starting Genai experiment...\n")


for run_number in range(1, NUM_RUNS + 1):

    print(f"Running {run_number}/{NUM_RUNS}")

    result = connector.generate(
        prompt=PROMPT,
        temperature=TEMPERATURE,
        seed=SEED
    )

    result["experiment_id"] = experiment_id
    result["run_number"] = run_number
    result["prompt_version"] = PROMPT_VERSION
    result["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    results.append(result)

    print(result["output"])
    print("-" * 40)


# Save results
Path("results").mkdir(exist_ok=True)

output_file = Path("results/day2_runs.jsonl")

with output_file.open("w", encoding="utf-8") as file:

    for result in results:
        file.write(json.dumps(result) + "\n")


print("\nExperiment completed!")
print(f"Saved {len(results)} runs.")
