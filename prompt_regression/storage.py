

from typing import List, Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, create_engine, Session, select

from prompt_regression.models import TestResult


class TestResultDB(SQLModel, table=True):
    """Database table for storing test results."""

    id: Optional[int] = Field(default=None, primary_key=True)
    test_name: str
    prompt: str
    output: str
    expected: Optional[str] = None
    similarity_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# create SQLite engine once so all sessions share the same database
engine = create_engine("sqlite:///results.db")


def init_db() -> None:
    """Initialize database and create tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


def save_results(results: List[TestResult]) -> None:
    """Save a list of TestResult objects into the database."""

    with Session(engine) as session:
        for result in results:
            # convert runtime object into DB row format
            db_row = TestResultDB(
                test_name=result.test_name,
                prompt=result.prompt,
                output=result.output,
                expected=result.expected,
                similarity_score=result.similarity_score,
            )
            session.add(db_row)

        # commit once after all inserts to improve performance and consistency
        session.commit()


def get_latest_results(test_name: str) -> List[TestResultDB]:
    """Fetch latest results for a given test name."""

    with Session(engine) as session:
        statement = (
            select(TestResultDB)
            .where(TestResultDB.test_name == test_name)
            .order_by(TestResultDB.created_at.desc())
        )

        results = session.exec(statement).all()

    return results