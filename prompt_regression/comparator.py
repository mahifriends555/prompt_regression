

from typing import List, Dict

from prompt_regression.models import TestResult
from prompt_regression.storage import get_latest_results


def compare_results(current_results: List[TestResult]) -> List[Dict]:
    """Compare current results with previous stored results."""

    comparisons: List[Dict] = []

    for result in current_results:
        # fetch past results for this test
        previous_runs = get_latest_results(result.test_name)

        if not previous_runs or previous_runs[0].similarity_score is None:
            # no baseline available → cannot compare
            comparisons.append({
                "test_name": result.test_name,
                "status": "no_baseline",
                "current_score": result.similarity_score,
                "previous_score": None,
                "delta": None
            })
            continue

        previous_score = previous_runs[0].similarity_score
        current_score = result.similarity_score

        # guard against missing scores
        if current_score is None or previous_score is None:
            status = "no_score"
            delta = None
        else:
            delta = current_score - previous_score

            # classify change to detect regressions/improvements
            if delta > 0.05:
                status = "improved"
            elif delta < -0.05:
                status = "regression"
            else:
                status = "no_change"

        comparisons.append({
            "test_name": result.test_name,
            "status": status,
            "current_score": current_score,
            "previous_score": previous_score,
            "delta": delta
        })

    return comparisons
