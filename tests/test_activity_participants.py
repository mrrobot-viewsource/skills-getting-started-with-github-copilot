import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app


def test_unregister_participant_from_activity():
    client = TestClient(app)

    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    chess_club = activities["Chess Club"]
    original_participants = list(chess_club["participants"])

    participant_to_remove = original_participants[0]

    delete_response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": participant_to_remove},
    )

    assert delete_response.status_code == 200
    assert participant_to_remove not in delete_response.json()["participants"]

    updated_response = client.get("/activities")
    updated_activities = updated_response.json()
    assert participant_to_remove not in updated_activities["Chess Club"]["participants"]
    assert len(updated_activities["Chess Club"]["participants"]) == len(original_participants) - 1
