
from typing import List

from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from prompt_regression.models import TestResult


def evaluate_with_deepeval(results: List[TestResult]) -> List[TestResult]:
    """Evaluate results using DeepEval metrics."""

    evaluated_results: List[TestResult] = []

    # initialize metric once to avoid repeated setup cost
    metric = AnswerRelevancyMetric()

    for result in results:
        if not result.expected:
            # skip evaluation if no expected answer
            evaluated_results.append(result)
            continue

        try:
            # create test case for DeepEval
            test_case = LLMTestCase(
                input=result.prompt,
                actual_output=result.output,
                expected_output=result.expected,
            )

            # measure quality using LLM-based evaluation
            score = metric.measure(test_case)

            # attach score (0–1 range)
            result.similarity_score = score

        except Exception as e:
            # avoid crashing entire pipeline if evaluation fails
            result.similarity_score = None

        evaluated_results.append(result)

    return evaluated_results