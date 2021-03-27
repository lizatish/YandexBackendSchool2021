import pytest
from sqlalchemy import create_engine

from store import create_app
from store.config import TestConfig


@pytest.fixture
def app(postgresql):
    app = create_app(TestConfig)

    return app


