from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_email_from_activity():
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    activity_data = client.get("/activities").json()[activity]
    assert email not in activity_data["participants"]


def test_delete_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
