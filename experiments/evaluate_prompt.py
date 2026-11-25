
import json
from pathlib import Path
from collections import Counter
from itertools import combinations

file_path = Path("results/day5_prompt_runs.jsonl")

runs = []

with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        runs.append(json.loads(line))

print("\nGENAI PROMPT SENSITIVITY REPORT")
print("=" * 45)

prompt_names = sorted(set(
    run["prompt_name"] for run in runs
))

report = {}

for prompt_name in prompt_names:

    outputs = [
        run["output"].strip()
        for run in runs
        if run["prompt_name"] == prompt_name
    ]

    counts = Counter(outputs)

    total = len(outputs)
    unique = len(counts)

    modal_score = (
        counts.most_common(1)[0][1] / total
    ) * 100

    pairs = list(combinations(outputs, 2))

    matching = sum(
        1 for a, b in pairs if a == b
    )

    pairwise_score = (
        matching / len(pairs) * 100
        if pairs else 0
    )

    report[prompt_name] = {
        "total_runs": total,
        "unique_outputs": unique,
        "modal_consistency": round(modal_score, 2),
        "pairwise_agreement": round(pairwise_score, 2)
    }

    print(f"\n{prompt_name}")
    print("Unique outputs:", unique)
    print("Modal consistency:", round(modal_score, 2), "%")
    print("Pairwise agreement:", round(pairwise_score, 2), "%")

# Save report

with open(
    "results/day5_prompt_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(report, file, indent=4)

print("\nReport saved successfully!")
