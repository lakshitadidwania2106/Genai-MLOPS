
import json
from pathlib import Path

file_path = Path("results/day6_structured_runs.jsonl")

EXPECTED_FIELDS = {
    "topic": str,
    "definition": str,
    "example": str,
    "key_points": list
}

runs = []

with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        runs.append(json.loads(line))

total_runs = len(runs)

valid_json_count = 0
schema_valid_count = 0
complete_fields_count = 0

for run in runs:

    output = run["output"].strip()

    try:
        data = json.loads(output)
        valid_json_count += 1

    except json.JSONDecodeError:
        print(f"Run {run['run_number']}: Invalid JSON")
        continue

    # Check required fields

    missing_fields = [
        field for field in EXPECTED_FIELDS
        if field not in data
    ]

    if not missing_fields:
        complete_fields_count += 1

    # Check field data types

    correct_types = all(
        isinstance(data.get(field), expected_type)
        for field, expected_type in EXPECTED_FIELDS.items()
    )

    # Check key_points contains exactly 3 strings

    valid_key_points = (
        isinstance(data.get("key_points"), list)
        and len(data["key_points"]) == 3
        and all(isinstance(point, str)
                for point in data["key_points"])
    )

    # Check no extra fields

    no_extra_fields = set(data.keys()) == set(
        EXPECTED_FIELDS.keys()
    )

    if correct_types and valid_key_points and no_extra_fields:
        schema_valid_count += 1

    print(f"\nRun {run['run_number']}")
    print("Missing fields:", missing_fields)
    print("Correct types:", correct_types)
    print("Valid key points:", valid_key_points)
    print("No extra fields:", no_extra_fields)

# Calculate metrics

def percentage(count, total):
    return round(count / total * 100, 2) if total else 0

report = {
    "total_runs": total_runs,
    "valid_json_rate": percentage(
        valid_json_count, total_runs
    ),
    "field_completeness_rate": percentage(
        complete_fields_count, total_runs
    ),
    "schema_validity_rate": percentage(
        schema_valid_count, total_runs
    )
}

print("\nGENAI STRUCTURED OUTPUT REPORT")
print("=" * 40)

for key, value in report.items():
    print(f"{key}: {value}")

with open(
    "results/day6_structured_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(report, file, indent=4)

print("\nReport saved successfully!")
