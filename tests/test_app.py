from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    body = response.json()
    assert "Removed" in body["message"]
