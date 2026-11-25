
import json
from pathlib import Path
from datetime import datetime, timezone

from app.connectors.ollama_connector import OllamaConnector

MODEL_NAME = "llama3.2:1b"
TEMPERATURE = 0.7
SEED = 42
NUM_RUNS = 3

TEST_PROMPTS = {
    "normal_json": """
    Return a JSON object with:
    name, age, city.
    Use realistic example information.
    Return only JSON.
    """,

    "many_fields": """
    Return ONLY a JSON object with exactly these
    10 fields:

    name, age, email, phone, city,
    country, college, degree, semester, cgpa.

    Every field must be present.
    Age and semester must be integers.
    CGPA must be a number.
    All other fields must be strings.
    """,

    "nested_json": """
    Return ONLY JSON with this structure:

    {
        "student": {
            "name": "string",
            "age": 20
        },
        "subjects": [
            {
                "name": "string",
                "marks": 90
            }
        ],
        "passed": true
    }

    Include exactly three subjects.
    """,

    "unknown_information": """
    Return ONLY a JSON object containing:

    name, age, birthplace, occupation.

    The person is a fictional individual.
    You have not been given any personal details.

    Do not invent unknown information.
    Use null for unknown values.
    Age must be an integer or null.
    """,

    "strict_types": """
    Return ONLY a JSON object with:

    product: string
    price: number
    available: boolean
    quantity: integer
    tags: array of exactly three strings

    Do not include additional fields.
    """
}

connector = OllamaConnector(MODEL_NAME)
results = []

print("GENAI STRUCTURED OUTPUT STRESS TEST")

for test_name, prompt in TEST_PROMPTS.items():

    print(f"\nTesting: {test_name}")

    for run_number in range(1, NUM_RUNS + 1):

        result = connector.generate(
            prompt=prompt,
            temperature=TEMPERATURE,
            seed=SEED
        )

        result["test_name"] = test_name
        result["run_number"] = run_number
        result["timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

        results.append(result)

        print(f"\nRun {run_number}")
        print(result["output"])
        print("-" * 40)

Path("results").mkdir(exist_ok=True)

with open(
    "results/day6_stress_test.jsonl",
    "w",
    encoding="utf-8"
) as file:

    for result in results:
        file.write(json.dumps(result) + "\n")

print("\nStress test completed!")
print("Total actual LLM calls:", len(results))
