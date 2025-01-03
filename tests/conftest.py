import pytest
from faker import Faker


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Faker."""
    return Faker()
