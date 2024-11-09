import argparse
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt

from autocorrect import LevenshteinAutoCorrect, AutoCorrect, MarkovAutoCorrect
from data import load_single_word_lookup_data_set


@dataclass
class ResearchResults:
    algorithm_name: str
    total_time: float
    correct_cases: int


def plot_results(results: list[ResearchResults]) -> None:
    fig, ax1 = plt.subplots(figsize=(10, 6))

    algorithm_names = [result.algorithm_name for result in results]
    total_times = [result.total_time for result in results]
    correct_cases = [result.correct_cases for result in results]

    x_positions = range(len(algorithm_names))

    ax1.bar(
        x_positions, total_times, color="skyblue", label="Total Time (s)", width=0.4
    )
    ax1.set_xlabel("Algorithm")
    ax1.set_ylabel("Total Time (s)", color="skyblue")
    ax1.tick_params(axis="y", labelcolor="skyblue")
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(algorithm_names)

    ax2 = ax1.twinx()
    ax2.plot(
        x_positions, correct_cases, color="orange", marker="o", label="Correct Cases"
    )
    ax2.set_ylabel("Correct Cases", color="orange")
    ax2.tick_params(axis="y", labelcolor="orange")

    fig.suptitle("Algorithm Performance")
    fig.tight_layout()

    plt.savefig("results.png")


def count_correct_fixes(cls: AutoCorrect, samples_count: int) -> int:
    sample = cls.load_test_set(samples_count)
    correct = 0
    for n, (i, row) in enumerate(sample.iterrows()):
        original = row["label"]
        misspelled = row["input"]
        
        fixed = cls.fix_word(misspelled)

        was_correct = fixed == original
        info = "CORRECT" if was_correct else "WRONG"
        print(f"'{fixed}' {info} {cls.name} {n+1}/{samples_count}")

        if fixed == original:
            correct += 1

    return correct


def run_tests(samples_count: int) -> list[ResearchResults]:
    auto_correct_classes = [
        # LevenshteinAutoCorrect(),
        MarkovAutoCorrect()
    ]
    tests_results = []

    for cls in auto_correct_classes:
        start_time = time.perf_counter()

        correct_fixes = count_correct_fixes(cls, samples_count)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        cls_results = ResearchResults(
            algorithm_name=cls.name,
            total_time=elapsed_time,
            correct_cases=correct_fixes,
        )
        tests_results.append(cls_results)

    return tests_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run research N samples")
    parser.add_argument("N", type=int, help="Number of samples to be testes")

    args = parser.parse_args()
    results = run_tests(args.N)

    plot_results(results)
