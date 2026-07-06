from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = {
        name: {
            key: (value.copy() if isinstance(value, list) else value)
            for key, value in activity.items()
        }
        for name, activity in activities.items()
    }

    yield

    activities.clear()
    activities.update(
        {
            name: {
                key: (value.copy() if isinstance(value, list) else value)
                for key, value in activity.items()
            }
            for name, activity in original_state.items()
        }
    )
