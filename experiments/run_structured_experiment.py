
import json
from pathlib import Path
from datetime import datetime, timezone

from app.connectors.ollama_connector import OllamaConnector

MODEL_NAME = "llama3.2:1b"
TEMPERATURE = 0.0
SEED = 42
NUM_RUNS = 5

PROMPT = """
Explain machine learning.

Return ONLY a valid JSON object.
Do not use markdown or code blocks.

The JSON must contain exactly these fields:

{
    "topic": "string",
    "definition": "string",
    "example": "string",
    "key_points": ["string", "string", "string"]
}

Make sure all fields are present.
"""

connector = OllamaConnector(MODEL_NAME)

results = []

print("GENAI STRUCTURED OUTPUT EXPERIMENT")
print("=" * 40)

for run_number in range(1, NUM_RUNS + 1):

    print(f"\nRunning {run_number}/{NUM_RUNS}")

    result = connector.generate(
        prompt=PROMPT,
        temperature=TEMPERATURE,
        seed=SEED
    )

    result["run_number"] = run_number
    result["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    results.append(result)

    print(result["output"])
    print("-" * 30)

Path("results").mkdir(exist_ok=True)

with open(
    "results/day6_structured_runs.jsonl",
    "w",
    encoding="utf-8"
) as file:

    for result in results:
        file.write(json.dumps(result) + "\n")

print("\nExperiment completed!")
print("Total runs:", len(results))
