
import json
from datetime import datetime, timezone
from pathlib import Path

from app.connectors.ollama_connector import OllamaConnector

MODEL_NAME = "llama3.2:1b"
TEMPERATURE = 0.3
SEED = 42
NUM_RUNS = 5

#different ways of asking the same question

PROMPTS = {
    "prompt_1": "Explain what machine learning is.",
    
    "prompt_2": "What is machine learning? Explain it in simple words.",
    
    "prompt_3": "Describe machine learning in exactly three simple sentences."
}

connector = OllamaConnector(MODEL_NAME)

all_results = []

print("GENAI PROMPT SENSITIVITY EXPERIMENT")
print("=" * 45)

for prompt_name, prompt_text in PROMPTS.items():

    print(f"\nTesting: {prompt_name}")

    for run_number in range(1, NUM_RUNS + 1):

        print(f"Run {run_number}/{NUM_RUNS}")

        result = connector.generate(
            prompt=prompt_text,
            temperature=TEMPERATURE,
            seed=SEED
        )

        result["prompt_name"] = prompt_name
        result["run_number"] = run_number
        result["timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

        all_results.append(result)

        print(result["output"])
        print("-" * 30)

Path("results").mkdir(exist_ok=True)

output_file = Path("results/day5_prompt_runs.jsonl")

with output_file.open("w", encoding="utf-8") as file:

    for result in all_results:
        file.write(json.dumps(result) + "\n")

print("\nExperiment completed!")
print("Total runs:", len(all_results))
print("Saved to:", output_file)
