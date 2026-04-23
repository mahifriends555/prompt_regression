
from typing import Optional
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a single prompt test case loaded from YAML."""
    
    name: str
    prompt: str
    expected: Optional[str] = None  # expected output is optional


@dataclass
class TestResult:
    """Represents the result of running a test case."""
    
    test_name: str
    prompt: str
    output: str
    expected: Optional[str] = None
    similarity_score: Optional[float] = None
    