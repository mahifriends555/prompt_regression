
from typing import List, Dict
from rich.console import Console
from rich.table import Table

from prompt_regression.models import TestResult

console = Console()


def display_results(results: List[TestResult], comparisons: List[Dict]) -> None:
    """Display test results along with regression comparison."""

    # create table with additional columns for comparison insights
    table = Table(title="Prompt Regression Results")

    table.add_column("Test Name", style="cyan")
    table.add_column("Similarity", justify="right")
    table.add_column("Prev Score", justify="right")
    table.add_column("Delta", justify="right")
    table.add_column("Status", justify="center")

    for result, comp in zip(results, comparisons):
        # format similarity safely
        current_score = (
            f"{result.similarity_score:.2f}"
            if result.similarity_score is not None
            else "N/A"
        )

        prev_score = (
            f"{comp['previous_score']:.2f}"
            if comp["previous_score"] is not None
            else "N/A"
        )

        delta = (
            f"{comp['delta']:.2f}"
            if comp["delta"] is not None
            else "N/A"
        )

        status = comp["status"]

        # color coding status to make regressions obvious at a glance
        if status == "improved":
            status_display = "[green]IMPROVED[/green]"
        elif status == "regression":
            status_display = "[red]REGRESSION[/red]"
        elif status == "no_change":
            status_display = "[yellow]NO CHANGE[/yellow]"
        else:
            status_display = "[white]N/A[/white]"

        table.add_row(
            result.test_name,
            current_score,
            prev_score,
            delta,
            status_display,
        )

    console.print(table)