import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app


def test_unregister_participant_from_activity():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"

    initial_response = client.get("/activities")
    assert initial_response.status_code == 200

    activities = initial_response.json()
    chess_club = activities[activity_name]
    original_participants = list(chess_club["participants"])
    participant_to_remove = original_participants[0]

    # Act
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant_to_remove},
    )
    updated_response = client.get("/activities")

    # Assert
    assert delete_response.status_code == 200
    assert participant_to_remove not in delete_response.json()["participants"]

    updated_activities = updated_response.json()
    assert participant_to_remove not in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == len(original_participants) - 1
