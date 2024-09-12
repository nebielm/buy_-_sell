import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import get_user_test, create_user
from app.tests.test_01_post import create_post


client = TestClient(app)


@pytest.fixture
def get_user_1234():
    """
    Fixture for creating a test user with username and password: '1234test'.
    """
    username = "1234test"
    password = "1234test"
    return create_user(username=username, password=password)


def test_failing_to_create_message(create_post: dict, get_user_1234: dict, get_user_test: dict):
    """
    Test case for failing to create a message due to insufficient permissions.
    """
    receiver_id = get_user_1234["user_data"]["id"]
    headers_receiver = get_user_test["headers"]
    user_id = create_post['user_id']
    post_id = create_post['id']
    response = client.post(
        f"/users/{user_id}/post/{post_id}/message",
        json={
          "message": "second test message",
          "receiver_id": receiver_id
        },
        headers=headers_receiver
    )
    assert response.status_code == 403  # post.user_id has to be first receiver


@pytest.fixture
def create_first_message(create_post: dict, get_user_1234: dict):
    """
    Fixture for creating the first test message.
    """
    user_id = get_user_1234['user_data']['id']
    headers_sender = get_user_1234["headers"]
    post_id = create_post['id']
    response = client.post(
        f"/users/{user_id}/post/{post_id}/message",
        json={
          "message": "first test message",
          "receiver_id": create_post["user_id"]
        },
        headers=headers_sender
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_second_message(create_post: dict, get_user_1234: dict, get_user_test: dict):
    """
    Fixture for creating the second test message.
    """
    receiver_id = get_user_1234['user_data']['id']
    headers_receiver = get_user_test["headers"]
    user_id = create_post['user_id']
    post_id = create_post['id']
    response = client.post(
        f"/users/{user_id}/post/{post_id}/message",
        json={
          "message": "second test message",
          "receiver_id": receiver_id
        },
        headers=headers_receiver
    )
    assert response.status_code == 200
    return response.json()


def test_get_created_message(create_first_message: dict, create_second_message: dict,
                             get_user_1234: dict, get_user_test: dict):
    """
    Test case for retrieving and comparing created messages.
    """
    user_id = create_first_message["sender_id"]
    post_id = create_first_message["post_id"]
    headers_sender = get_user_1234["headers"]
    headers_receiver = get_user_test["headers"]
    response_first_message = client.get(f"/users/{user_id}/post/{post_id}/message",
                                        headers=headers_sender)
    assert response_first_message.status_code == 200
    first_message_response_data = response_first_message.json()
    user_id = create_second_message["sender_id"]
    post_id = create_second_message["post_id"]
    response_second_message = client.get(f"/users/{user_id}/post/{post_id}/message",
                                         headers=headers_receiver)
    assert response_second_message.status_code == 200
    second_message_response_data = response_second_message.json()
    sorted_first_response = sorted(first_message_response_data, key=lambda x: x['sender_id'])
    sorted_second_response = sorted(second_message_response_data, key=lambda x: x['sender_id'])
    assert sorted_first_response == sorted_second_response


def test_update_message(create_post: dict, create_first_message: dict, get_user_1234: dict):
    """
    Test case for updating an existing message.
    """
    user_id = create_first_message['sender_id']
    headers_sender = get_user_1234["headers"]
    message_id = create_first_message['id']
    updated_message = "updated message test"
    response = client.put(
        f"/users/{user_id}/messages/{message_id}/",
        headers=headers_sender,
        json={"message": updated_message}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["message"] == updated_message
