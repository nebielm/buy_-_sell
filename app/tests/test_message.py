import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def get_access_token_test():
    username = "test1234"
    password = "test1234"
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


access_token_sender = get_access_token_test()
headers_sender = {"Authorization": f"Bearer {access_token_sender}"}  # 2


def get_access_token_1234():
    username = "1234test"
    password = "1234test"
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


access_token_receiver = get_access_token_1234()
headers_receiver = {"Authorization": f"Bearer {access_token_receiver}"}  # 3


@pytest.fixture
def create_post():
    user_id = 3
    response = client.get(f"/users/{user_id}/posts/",
                          headers=headers_receiver
                          )
    to_delete = response.json()
    if to_delete:
        for post in to_delete:
            post_id = post['id']
            client.delete(f"/posts/{post_id}/",
                          headers=headers_receiver
                          )
    response = client.post(
        f"/users/{user_id}/posts/",
        json={
          "title": "test1234",
          "description": "test1234",
          "price": 2.0,
          "condition": "test1234",
          "status": "available",
          "user_id": user_id,
          "sub_category_id": 139
        },
        headers=headers_receiver
    )
    assert response.status_code == 200
    return response.json()


def test_failing_to_create_message(create_post):
    user_id = create_post['user_id']
    post_id = create_post['id']
    response = client.post(
        f"/users/{user_id}/post/{post_id}/message",
        json={
          "message": "second test message",
          "receiver_id": 2
        },
        headers=headers_receiver
    )
    assert response.status_code == 403  # post.user_id has to be first receiver


@pytest.fixture
def create_first_message(create_post):
    user_id = 2
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
def create_second_message(create_post):
    user_id = create_post['user_id']
    post_id = create_post['id']
    response = client.post(
        f"/users/{user_id}/post/{post_id}/message",
        json={
          "message": "second test message",
          "receiver_id": 2
        },
        headers=headers_receiver
    )
    assert response.status_code == 200
    return response.json()


def test_get_created_message(create_first_message, create_second_message):
    user_id = create_first_message["sender_id"]
    post_id = create_first_message["post_id"]
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


def test_update_message(create_post, create_first_message):
    user_id = create_first_message['sender_id']
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
