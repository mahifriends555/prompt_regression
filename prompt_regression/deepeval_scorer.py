
import os
from unittest import result
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
                model="gpt-4o",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": ("""
                                You are a strict evaluator.

                                Score the actual answer compared to the expected answer using:

                                1.0 = perfect match or meaning equivalent  
                                0.8–0.9 = mostly correct, minor differences  
                                0.5–0.7 = partially correct  
                                0.0–0.4 = incorrect or unrelated  
                                    
                                Be strict. Do not give 1.0 unless answers are almost identical.

                                Return ONLY a number between 0 and 1.
                                """
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
            # result.similarity_score = float(score_text)
            score = float(score_text.split()[0])
            result.similarity_score = score

        except Exception as e:
            print(f"Scoring error: {e}")
            result.similarity_score = None

    return results