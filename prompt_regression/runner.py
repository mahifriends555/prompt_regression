
from typing import List
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from prompt_regression.models import TestCase, TestResult

load_dotenv()


def run_test_case(test_case: TestCase) -> List[TestResult]:
    """Run a test case on multiple models (GPT + Gemini)."""

    results: List[TestResult] = []

    # --- GPT MODEL ---
    gpt = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    try:
        gpt_response = gpt.invoke(test_case.prompt)

        results.append(
            TestResult(
                test_name=f"{test_case.name}_gpt",
                prompt=test_case.prompt,
                output=gpt_response.content,
                expected=test_case.expected,
            )
        )
    except Exception as e:
        # ensure failure doesn't break pipeline
        results.append(
            TestResult(
                test_name=f"{test_case.name}_gpt",
                prompt=test_case.prompt,
                output=f"ERROR: {str(e)}",
                expected=test_case.expected,
            )
        )

    # --- GEMINI MODEL ---
    google_key = os.getenv("GOOGLE_API_KEY")

    if google_key:
        try:
            gemini = ChatGoogleGenerativeAI(
                model="gemini-flash-latest",
                temperature=0
            )

            # call Gemini
            gemini_response = gemini.invoke(test_case.prompt)

            content = gemini_response.content

            # normalize output to string (VERY IMPORTANT)
            if isinstance(content, list):
                texts = []
                for part in content:
                    if isinstance(part, dict):
                        text = part.get("text") or part.get("content") or ""
                        texts.append(text)
                output_text = " ".join(texts).strip()
            else:
                output_text = str(content).strip()

            # fallback if empty
            if not output_text:
                output_text = "EMPTY_RESPONSE"

            # debug (optional)
            print("GEMINI CONTENT:", output_text)

            results.append(
                TestResult(
                    test_name=f"{test_case.name}_gemini",
                    prompt=test_case.prompt,
                    output=output_text,
                    expected=test_case.expected,
                )
            )

        except Exception as e:
            # capture Gemini failure but continue pipeline
            print(f"GEMINI ERROR: {e}")
            results.append(
                TestResult(
                    test_name=f"{test_case.name}_gemini",
                    prompt=test_case.prompt,
                    output=f"ERROR: {str(e)}",
                    expected=test_case.expected,
                )
            )

    # ✅ CRITICAL: ALWAYS RETURN
    return results


def run_all_tests(test_cases: List[TestCase]) -> List[TestResult]:
    """Run all tests across models."""

    all_results: List[TestResult] = []

    for test in test_cases:
        results = run_test_case(test)

        # ensure we never extend with None
        if results:
            all_results.extend(results)

    return all_results