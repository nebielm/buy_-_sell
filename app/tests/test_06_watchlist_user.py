import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import create_user


client = TestClient(app)


def get_access_token(username, password):
    response = client.post(
        url="/token",
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
def get_followed_user():
    username = "1234test"
    password = "1234test"
    return create_user(username=username, password=password)


@pytest.fixture
def created_watch_user(get_following_user, get_followed_user):
    following_user_id = get_following_user['user_data']['id']
    followed_user_id = get_followed_user['user_data']['id']
    headers_following = get_following_user['headers']
    response = client.get(url=f"/following_user/{following_user_id}/watchlist/",
                          headers=headers_following
                          )
    to_delete = response.json()
    if response.status_code == 200:
        for record in to_delete:
            watch_user_id = record['id']
            client.delete(url=f"/following_user/{following_user_id}/watchlist/{watch_user_id}/",
                          headers=headers_following
                          )
    response = client.post(
        f"/following_user/{following_user_id}/watchlist/followed_user/{followed_user_id}/",
        headers=headers_following
    )
    assert response.status_code == 200
    return response.json()


def test_get_watch_user_by_followed_user(created_watch_user, get_followed_user):
    followed_user_id = created_watch_user['followed_user_id']
    headers_followed = get_followed_user['headers']
    response = client.get(
        f"/followed_user/{followed_user_id}/watchlist/",
        headers=headers_followed
    )
    response_data = response.json()
    assert created_watch_user in response_data


def test_get_watch_user_by_following_user(created_watch_user, get_following_user):
    following_user_id = created_watch_user['following_user_id']
    headers_following = get_following_user['headers']
    response = client.get(
        f"/following_user/{following_user_id}/watchlist/",
        headers=headers_following
    )
    response_data = response.json()
    assert created_watch_user in response_data


def test_get_watch_user_by_id(created_watch_user, get_following_user):
    following_user_id = created_watch_user['following_user_id']
    headers_following = get_following_user['headers']
    watch_user_id = created_watch_user['id']
    response = client.get(
        f"/following_user/{following_user_id}/watchlist/{watch_user_id}/",
        headers=headers_following
    )
    response_data = response.json()
    assert response_data == created_watch_user
