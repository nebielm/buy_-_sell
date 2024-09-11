import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import get_user_test


client = TestClient(app)


def create_a_post(user):
    headers = user['headers']
    user_id = user['user_data']['id']
    response = client.get(url=f"/users/{user_id}/posts/",
                          headers=headers
                          )
    to_delete = response.json()
    if to_delete:
        for post in to_delete:
            post_id = post['id']
            client.delete(url=f"/posts/{post_id}/",
                          headers=headers
                          )
    response = client.post(
        url=f"/users/{user_id}/posts/",
        json={
          "title": "test1234Post",
          "description": "test1234Post",
          "price": 2.0,
          "condition": "test1234Post",
          "quantity": 10,
          "status": "available",
          "user_id": user_id,
          "sub_category_id": 139
        },
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_post(get_user_test):
    return create_a_post(get_user_test)


def test_get_post(create_post, get_user_test):
    headers = get_user_test['headers']
    user_id = create_post["user_id"]
    response = client.get(
        f"/users/{user_id}/posts/",
        headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()
    for post in response_data:
        post.pop('created_at', None)
    expected_response = {
        "title": "test1234Post",
        "use_payment_option": True,
        "description": "test1234Post",
        "price": 2.0,
        "condition": "test1234Post",
        "quantity": 10,
        "pick_up": False,
        "status": "available",
        "show_email": True,
        "show_tel": True,
        "id": create_post['id'],
        "user_id": user_id,
        "sub_category_id": 139
      }
    assert expected_response in response_data


def test_failing_update_post(get_user_test):
    headers = get_user_test['headers']
    post_id = 0
    response = client.put(
        f"/posts/{post_id}/",
        json={
         "title": "string",
         "use_payment_option": False,
         "description": "string",
         "price": 1.0,
         "condition": "string"
        },
        headers=headers
    )
    assert response.status_code == 404
    assert response.json() == {
      "detail": "Post not found"
    }


def test_update_post(create_post, get_user_test):
    headers = get_user_test['headers']
    user_id = create_post["user_id"]
    post_id = create_post['id']
    response = client.put(
        f"/posts/{post_id}/",
        json={
            "title": "test1234Post",
            "use_payment_option": False,
            "description": "test1234Post",
            "price": 1.0,
            "condition": "test1234Post"
        },
        headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()
    response_data.pop("created_at", None)
    assert response_data == {
      "title": "test1234Post",
      "use_payment_option": False,
      "description": "test1234Post",
      "price": 1.0,
      "condition": "test1234Post",
      "quantity": 10,
      "pick_up": False,
      "status": "available",
      "show_email": True,
      "show_tel": True,
      "id": post_id,
      "user_id": user_id,
      "sub_category_id": 139
    }
