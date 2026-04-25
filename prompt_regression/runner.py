
import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from prompt_regression.models import TestCase, TestResult

# load environment variables once so API keys are available
load_dotenv()


def run_test_case(test_case: TestCase) -> TestResult:
    """Run a single test case against the LLM and return the result."""

    # ensure API key exists before making a costly API call
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    # initialize LLM client each call to keep function stateless and predictable
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0  # deterministic output for testing
    )

    try:
        # call the model with the prompt
        response = llm.invoke(test_case.prompt)

        # extract text content safely
        output_text = response.content

    except Exception as e:
        # catch API or network errors so one failure doesn't crash entire run
        raise RuntimeError(f"LLM call failed for test '{test_case.name}': {str(e)}")

    # return structured result for downstream modules
    return TestResult(
        test_name=test_case.name,
        prompt=test_case.prompt,
        output=output_text,
        expected=test_case.expected,
    )



def run_all_tests(test_cases: List[TestCase]) -> List[TestResult]:
    """Run multiple test cases independently and collect results."""

    results: List[TestResult] = []

    # run each test independently so one failure does not stop the rest
    for test in test_cases:
        try:
            result = run_test_case(test)
            results.append(result)
        except Exception as e:
            # capture failure as a result-like record instead of crashing
            results.append(
                TestResult(
                    test_name=test.name,
                    prompt=test.prompt,
                    output=f"ERROR: {str(e)}",
                    expected=test.expected,
                )
            )

    return results

