
    # check file exists
    # open and load yaml
    # validate structure
    # loop and convert
    # return list

import os
import yaml
from typing import List
from prompt_regression.models import TestCase


def load_test_cases(file_path: str) -> List[TestCase]:
    """Load test cases from a YAML file and return a list of TestCase objects."""

    # ensure the file actually exists before trying to open it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test file not found: {file_path}")

    # ensure we only process YAML files to avoid unexpected formats
    if not file_path.endswith(".yaml"):
        raise ValueError("Only YAML files are supported.")

    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    # ensure YAML contains a list of test cases
    if not isinstance(data, list):
        raise ValueError("YAML file must contain a list of test cases.")

    test_cases: List[TestCase] = []

    for idx, case in enumerate(data):
        # validate required fields early to give clear error messages
        if "name" not in case or "prompt" not in case:
            raise ValueError(f"Missing required fields in test case at index {idx}")

        # create structured object so rest of system can rely on consistent shape
        test_cases.append(
            TestCase(
                name=case["name"],
                prompt=case["prompt"],
                expected=case.get("expected"),
            )
        )

    return test_cases
