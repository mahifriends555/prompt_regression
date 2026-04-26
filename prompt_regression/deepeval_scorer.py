
import os
from openai import OpenAI
from typing import List
from prompt_regression.models import TestResult

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_with_deepeval(results: List[TestResult]) -> List[TestResult]:
    """LLM-as-judge scoring using OpenAI directly."""

    for result in results:
        if not result.expected:
            continue

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict evaluator. Given an expected answer and an actual answer, "
                            "score the actual answer from 0.0 to 1.0 based on correctness. "
                            "Reply with ONLY a number, nothing else."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Expected: {result.expected}\n"
                            f"Actual: {result.output}\n"
                            f"Score:"
                        ),
                    },
                ],
            )

            score_text = response.choices[0].message.content.strip()
            result.similarity_score = float(score_text)

        except Exception as e:
            print(f"Scoring error: {e}")
            result.similarity_score = None

    return results