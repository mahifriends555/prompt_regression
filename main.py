
from prompt_regression.config_loader import load_test_cases
from prompt_regression.runner import run_all_tests
from prompt_regression.storage import init_db, save_results
from prompt_regression.scorer import score_results
from prompt_regression.comparator import compare_results
from prompt_regression.reporter import display_results
from prompt_regression.deepeval_scorer import evaluate_with_deepeval

def main() -> None:
    """Run the full prompt regression pipeline."""

    # load test cases from YAML so we can define tests without changing code
    test_cases = load_test_cases("data/tests.yaml")

    # run prompts through LLM to generate outputs
    results = run_all_tests(test_cases)

    # initialize database before saving anything
    init_db()

    # compute similarity scores before saving so DB has full data
    scored_results = evaluate_with_deepeval(results)

    # store results for future comparison
    save_results(scored_results)

    # compare current run with previous runs to detect regressions
    comparisons = compare_results(scored_results)

    # display final results with comparison insights
    display_results(scored_results, comparisons)


if __name__ == "__main__":
    main()