
import json
from collections import Counter
from itertools import combinations

INPUT_FILE = "results/day8_controlled_runs.jsonl"


def load_results():

    results = []

    with open(INPUT_FILE, "r") as file:
        for line in file:
            results.append(json.loads(line))

    return results


def calculate_metrics(outputs):

    total = len(outputs)

    if total == 0:
        return {}

    counts = Counter(outputs)

    unique_count = len(counts)

    modal_consistency = max(counts.values()) / total

    pairs = list(combinations(outputs, 2))

    if pairs:
        matching_pairs = sum(
            1 for a, b in pairs if a == b
        )

        pairwise_agreement = matching_pairs / len(pairs)

    else:
        pairwise_agreement = 1.0

    return {
        "total_runs": total,
        "unique_outputs": unique_count,
        "modal_consistency": round(modal_consistency, 4),
        "pairwise_agreement": round(pairwise_agreement, 4)
    }


def evaluate_groups(results):

    groups = {}

    for result in results:

        if result["experiment"] == "temperature":
            key = (
                "temperature",
                result["temperature"],
                result["seed"]
            )

        else:
            key = (
                "seed",
                result["seed"],
                result["temperature"]
            )

        groups.setdefault(key, []).append(result)

    for key, runs in groups.items():

        outputs = [
            run["output"].strip()
            for run in runs
        ]

        metrics = calculate_metrics(outputs)

        latencies = [
            run["latency_seconds"]
            for run in runs
        ]

        average_latency = sum(latencies) / len(latencies)

        print("\nExperiment:", key[0])
        print("Configuration:", key[1:])
        print("Metrics:", metrics)
        print(
            "Average latency:",
            round(average_latency, 4),
            "seconds"
        )

def compare_across_configurations(results, experiment_name, parameter):

    groups = {}

    for result in results:

        if result["experiment"] == experiment_name:

            value = result[parameter]

            groups.setdefault(value, []).append(
                result["output"].strip()
            )

    print("\nCROSS-CONFIGURATION COMPARISON:", experiment_name)

    representatives = {}

    for value, outputs in sorted(groups.items()):

        unique = set(outputs)

        print(
            parameter, value,
            "| Unique outputs:", len(unique)
        )

        if len(unique) == 1:
            representatives[value] = outputs[0]

    all_unique = set(representatives.values())

    print(
        "Unique outputs across configurations:",
        len(all_unique)
    )

    for value, output in representatives.items():

        print("\nConfiguration:", value)
        print("Output:", output[:200])


if __name__ == "__main__":

    results = load_results()

    print("Total model calls:", len(results))

    evaluate_groups(results)
    
    compare_across_configurations(
    results, "temperature", "temperature"
)

compare_across_configurations(
    results, "seed", "seed"
)
