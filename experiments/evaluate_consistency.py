
import json
from pathlib import Path
from collections import Counter
from itertools import combinations

file_path = Path("results/day2_runs.jsonl")

runs = []
with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        runs.append(json.loads(line))

outputs = [run["output"].strip() for run in runs]

output_counts = Counter(outputs) #get the unique output

total_runs = len(outputs)
unique_outputs = len(output_counts)

most_common_output, frequency = output_counts.most_common(1)[0]

modal_consistency = frequency / total_runs #see if model is consistent

pairs = list(combinations(outputs, 2))

matching_pairs = sum(
    1 for a, b in pairs if a == b
)

pairwise_agreement = matching_pairs / len(pairs) if pairs else 0

all_identical = unique_outputs == 1 #is every ouput same?


report = {
    "total_runs": total_runs,
    "unique_outputs": unique_outputs,
    "modal_consistency": round(modal_consistency * 100, 2),
    "pairwise_agreement": round(pairwise_agreement * 100, 2),
    "all_outputs_identical": all_identical
}

print("\nGENAI CONSISTENCY REPORT")
print("-" * 35)

for key, value in report.items():
    print(f"{key}: {value}")

Path("results").mkdir(exist_ok=True) #save report

with open("results/day3_consistency_report.json", "w") as file:
    json.dump(report, file, indent=4)

print("\nReport saved successfully!")
