import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import create_user


client = TestClient(app)


def get_access_token(username, password):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def get_following_user():
    username = "test1234"
    password = "test1234"
    return create_user(username=username, password=password)


@pytest.fixture
def get_post_user():
    username = "1234test"
    password = "1234test"
    return create_user(username=username, password=password)


@pytest.fixture
def create_post(get_post_user):
    user_id = get_post_user['user_data']['id']
    post_headers = get_post_user['headers']
    response = client.get(f"/users/{user_id}/posts/",
                          headers=post_headers
                          )
    to_delete = response.json()
    if to_delete:
        for post in to_delete:
            post_id = post['id']
            client.delete(url=f"/posts/{post_id}/",
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
          "user_id": user_id,
          "sub_category_id": 139
        },
        headers=post_headers
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_watch_post(create_post, get_following_user):
    user_id = get_following_user['user_data']["id"]
    headers = get_following_user['headers']
    post_id = create_post['id']
    response = client.post(
        f"/user/{user_id}/watchlist/post/{post_id}/",
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


def test_get_watch_posts_by_followed_post(create_watch_post, get_post_user):
    user_id = get_post_user['user_data']['id']
    post_headers = get_post_user['headers']
    post_id = create_watch_post['followed_post_id']
    response = client.get(
        f"/user/{user_id}/watchlist/post/{post_id}/",
        headers=post_headers
    )
    response_data = response.json()
    assert create_watch_post in response_data


def test_get_watch_posts_by_following_user(create_watch_post, get_following_user):
    user_id = get_following_user['user_data']["id"]
    headers = get_following_user['headers']
    response = client.get(
        f"/user/{user_id}/watchlist/",
        headers=headers
    )
    response_data = response.json()
    assert create_watch_post in response_data


def test_get_watch_posts_by_id(create_post, create_watch_post, get_following_user):
    user_id = get_following_user['user_data']["id"]
    headers = get_following_user['headers']
    watch_post_id = create_watch_post['id']
    response = client.get(
        f"/user/{user_id}/watchlist/{watch_post_id}/",
        headers=headers
    )
    response_data = response.json()
    assert create_watch_post == response_data
