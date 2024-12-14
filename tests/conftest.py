"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pytest
from faker import Faker


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Faker."""
    return Faker()
