
import json
from pathlib import Path
from collections import Counter
from itertools import combinations

file_path = Path("results/day4_temperature_runs.jsonl")

runs = []

with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        runs.append(json.loads(line))

print("\nGENAI TEMPERATURE COMPARISON")
print("=" * 45)

temperatures = sorted(set(
    run["temperature"] for run in runs
))

report = {}

for temperature in temperatures:

    outputs = [
        run["output"].strip()
        for run in runs
        if run["temperature"] == temperature
    ]

    counts = Counter(outputs)

    total = len(outputs)
    unique = len(counts)

    most_common_frequency = counts.most_common(1)[0][1]

    modal_consistency = (
        most_common_frequency / total
    ) * 100

    pairs = list(combinations(outputs, 2))

    matching_pairs = sum(
        1 for a, b in pairs if a == b
    )

    pairwise_agreement = (
        matching_pairs / len(pairs) * 100
        if pairs else 0
    )

    report[str(temperature)] = {
        "total_runs": total,
        "unique_outputs": unique,
        "modal_consistency": round(
            modal_consistency, 2
        ),
        "pairwise_agreement": round(
            pairwise_agreement, 2
        )
    }

    print(f"\nTemperature: {temperature}")
    print("Unique outputs:", unique)
    print("Modal consistency:", round(
        modal_consistency, 2
    ), "%")
    print("Pairwise agreement:", round(
        pairwise_agreement, 2
    ), "%")

with open(
    "results/day4_temperature_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(report, file, indent=4)

print("\nComparison report saved!")
