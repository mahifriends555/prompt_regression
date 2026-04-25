
from typing import List
from sentence_transformers import SentenceTransformer, util

from prompt_regression.models import TestResult

# load model once globally so we don't reload it for every function call
model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(text1: str, text2: str) -> float:
    """Compute semantic similarity between two text strings."""

    # guard against empty inputs which would break embedding model
    if not text1 or not text2:
        return 0.0

    # convert texts into vector embeddings
    embeddings = model.encode([text1, text2], convert_to_tensor=True)

    # compute cosine similarity between embeddings
    score = util.cos_sim(embeddings[0], embeddings[1])

    return float(score.item())


def score_results(results: List[TestResult]) -> List[TestResult]:
    """Attach similarity scores to each TestResult."""

    scored_results: List[TestResult] = []

    # process each result independently to avoid cascading failures
    for result in results:
        if result.expected:
            similarity = compute_similarity(result.output, result.expected)
        else:
            # if no expected answer, we cannot compute similarity
            similarity = None

        # create updated result object with score
        scored_results.append(
            TestResult(
                test_name=result.test_name,
                prompt=result.prompt,
                output=result.output,
                expected=result.expected,
                similarity_score=similarity,
            )
        )

    return scored_results

if __name__ == "__main__":
    # example usage
    test_result = TestResult(
        test_name="Example Test",
        prompt="What is the capital of France?",
        output="The capital of France is Paris.",
        expected="Paris is the capital of France."
    )

    scored = score_results([test_result])
    print(scored[0])