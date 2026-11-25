
import json
from pathlib import Path

# Load actual LLM responses

file_path = Path("results/day6_stress_test.jsonl")

runs = []

with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        runs.append(json.loads(line))


# Expected schemas for each test

SCHEMAS = {
    "normal_json": {
        "name": str,
        "age": int,
        "city": str
    },

    "many_fields": {
        "name": str,
        "age": int,
        "email": str,
        "phone": str,
        "city": str,
        "country": str,
        "college": str,
        "degree": str,
        "semester": int,
        "cgpa": float
    },

    "nested_json": {
        "student": dict,
        "subjects": list,
        "passed": bool
    },

    "unknown_information": {
        "name": str,
        "age": (str, int, type(None)),
        "birthplace": str,
        "occupation": str
    },

    "strict_types": {
        "product": str,
        "price": (int, float),
        "available": bool,
        "quantity": int,
        "tags": list
    }
}


def extract_json(output):
    """
    Extract the first JSON object from the LLM response.
    Also identify text surrounding the JSON.
    """

    start = output.find("{")

    if start == -1:
        return None, False

    try:
        data, end = json.JSONDecoder().raw_decode(
            output[start:]
        )

        prefix = output[:start].strip()
        suffix = output[start + end:].strip()

        # Markdown fences are wrappers, not JSON-only output
        raw_json_only = (
            prefix == "" and suffix == ""
        )

        return data, raw_json_only

    except json.JSONDecodeError:
        return None, False


def check_nested(data):

    if not isinstance(data.get("student"), dict):
        return False

    if not isinstance(data.get("subjects"), list):
        return False

    student = data["student"]
    subjects = data["subjects"]

    if set(student.keys()) != {"name", "age"}:
        return False

    if type(student["name"]) is not str:
        return False

    if type(student["age"]) is not int:
        return False

    if len(subjects) != 3:
        return False

    for subject in subjects:
        if not isinstance(subject, dict):
            return False

        if set(subject.keys()) != {"name", "marks"}:
            return False

        if type(subject["name"]) is not str:
            return False

        if type(subject["marks"]) is not int:
            return False

    return type(data.get("passed")) is bool


def check_task_compliance(test_name, data):

    # The unknown-information task explicitly forbids invention.
    if test_name == "unknown_information":
        return all(
            data.get(field) is None
            for field in [
                "name", "age", "birthplace", "occupation"
            ]
        )

    # Exactly three string tags are required.
    if test_name == "strict_types":
        tags = data.get("tags")

        return (
            isinstance(tags, list)
            and len(tags) == 3
            and all(type(tag) is str for tag in tags)
        )

    # Exactly three subjects are required.
    if test_name == "nested_json":
        return check_nested(data)

    return True


# Evaluate every run

results = []

for run in runs:

    test_name = run["test_name"]
    output = run["output"].strip()

    data, raw_json_only = extract_json(output)

    valid_json = isinstance(data, dict)

    schema = SCHEMAS[test_name]

    missing = []
    extra = []
    correct_types = False
    task_compliant = False

    if valid_json:

        missing = [
            field for field in schema
            if field not in data
        ]

        extra = [
            field for field in data
            if field not in schema
        ]

        correct_types = all(
            field in data and
            type(data[field]) in (
                expected if isinstance(expected, tuple)
                else (expected,)
            )
            for field, expected in schema.items()
        )

        task_compliant = check_task_compliance(
            test_name, data
        )

    schema_valid = (
        valid_json
        and len(missing) == 0
        and len(extra) == 0
        and correct_types
    )

    result = {
        "test_name": test_name,
        "run_number": run["run_number"],
        "valid_json": valid_json,
        "raw_json_only": raw_json_only,
        "missing_fields": missing,
        "extra_fields": extra,
        "correct_types": correct_types,
        "schema_valid": schema_valid,
        "task_compliant": task_compliant
    }

    results.append(result)

    print(f"\n{test_name} - Run {run['run_number']}")
    print("Valid JSON:", valid_json)
    print("Raw JSON only:", raw_json_only)
    print("Missing fields:", missing)
    print("Extra fields:", extra)
    print("Correct types:", correct_types)
    print("Schema valid:", schema_valid)
    print("Task compliant:", task_compliant)


# Calculate overall metrics

total = len(results)

def percentage(count):
    return round(count / total * 100, 2) if total else 0


report = {
    "total_runs": total,
    "valid_json_rate": percentage(
        sum(r["valid_json"] for r in results)
    ),
    "raw_json_only_rate": percentage(
        sum(r["raw_json_only"] for r in results)
    ),
    "schema_validity_rate": percentage(
        sum(r["schema_valid"] for r in results)
    ),
    "task_compliance_rate": percentage(
        sum(r["task_compliant"] for r in results)
    )
}

print("\nGENAI RELIABILITY REPORT")
print("=" * 40)

for metric, value in report.items():
    print(f"{metric}: {value}")

# Save detailed report

Path("results").mkdir(exist_ok=True)

with open(
    "results/day6_stress_test_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        {
            "summary": report,
            "individual_results": results
        },
        file,
        indent=4
    )

print("\nDetailed report saved!")
