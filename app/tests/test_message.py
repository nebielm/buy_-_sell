import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def get_access_token():
    username = "mnebiel"
    password = "1234567890"
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


access_token = get_access_token()
headers = {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def created_message():
    user_id = 1
    post_id = 1
    response = client.post(
        f"/users/{user_id}/post/{post_id}/message",
        json={"message": "test", "sender_id": user_id, "receiver_id": 2, "post_id": post_id},
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


def test_created_message(created_message):
    user_id = 1
    post_id = 1
    assert "id" in created_message
    assert "last_message_change" in created_message
    assert created_message["message"] == "test"
    assert created_message["sender_id"] == user_id
    assert created_message["receiver_id"] == 2
    assert created_message["post_id"] == post_id


def test_update_message(created_message):
    user_id = 1
    post_id = 1
    message_id = created_message['id']
    new_message = "updated message"
    response = client.put(
        f"/users/{user_id}/messages/{message_id}/",
        headers=headers,
        json={"message": new_message}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == message_id
    assert "last_message_change" in json_response
    assert json_response["message"] == new_message
    assert json_response["sender_id"] == user_id
    assert json_response["receiver_id"] == 2
    assert json_response["post_id"] == post_id
