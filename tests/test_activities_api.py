import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def restore_activities():
    # Make a deep copy of activities to restore after each test
    import copy
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure one known activity exists
    assert "Chess Club" in data

def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure email not already in participants
    assert email not in activities[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

def test_unregister_nonexistent_activity():
    resp = client.delete("/activities/NotAnActivity/participants?email=foo@example.com")
    assert resp.status_code == 404

def test_unregister_nonexistent_participant():
    activity = "Chess Club"
    resp = client.delete(f"/activities/{activity}/participants?email=notreal@example.com")
    assert resp.status_code == 404
