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


post_access_token = get_access_token_test()
post_headers = {"Authorization": f"Bearer {post_access_token}"}


def get_access_token_1234():
    username = "1234test"
    password = "1234test"
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


access_token = get_access_token_1234()
headers = {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def created_post():
    user_id = 2
    response = client.get(f"/users/{user_id}/posts/",
                          headers=post_headers
                          )
    to_delete = response.json()
    for post in to_delete:
        post_id = post['id']
        client.delete(f"/posts/{post_id}/",
                      headers=post_headers
                      )
    response = client.post(
        f"/users/{user_id}/posts/",
        json={
          "title": "test1234Post",
          "description": "test1234Post",
          "price": 2.0,
          "condition": "test1234Post",
          "status": "available",
          "user_id": 2,
          "sub_category_id": 139
        },
        headers=post_headers
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def created_watch_post(created_post):
    user_id = 3
    post_id = created_post['id']
    response = client.post(
        f"/user/{user_id}/watchlist/post/{post_id}/",
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


def test_get_watch_posts_by_followed_post(created_watch_post):
    user_id = 2
    post_id = created_watch_post['followed_post_id']
    response = client.get(
        f"/user/{user_id}/watchlist/post/{post_id}/",
        headers=post_headers
    )
    response_data = response.json()
    assert created_watch_post in response_data


def test_get_watch_posts_by_following_user(created_watch_post):
    user_id = 3
    response = client.get(
        f"/user/{user_id}/watchlist/",
        headers=headers
    )
    response_data = response.json()
    assert created_watch_post in response_data


def test_get_watch_posts_by_id(created_post, created_watch_post):
    user_id = 3
    watch_post_id = created_watch_post['id']
    response = client.get(
        f"/user/{user_id}/watchlist/{watch_post_id}/",
        headers=headers
    )
    response_data = response.json()
    assert created_watch_post == response_data
