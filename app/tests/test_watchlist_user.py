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


access_token_followed = get_access_token_test()
headers_followed = {"Authorization": f"Bearer {access_token_followed}"}  # 2


def get_access_token_1234():
    username = "1234test"
    password = "1234test"
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


access_token_following = get_access_token_1234()
headers_following = {"Authorization": f"Bearer {access_token_following}"}  # 3


@pytest.fixture
def created_watch_user():
    following_user_id = 3
    followed_user_id = 2
    response = client.get(f"/following_user/{following_user_id}/watchlist/",
                          headers=headers_following
                          )
    to_delete = response.json()
    for record in to_delete:
        watch_user_id = record['id']
        client.delete(f"/following_user/{following_user_id}/watchlist/{watch_user_id}/",
                      headers=headers_following
                      )
    response = client.post(
        f"/following_user/{following_user_id}/watchlist/followed_user/{followed_user_id}/",
        headers=headers_following
    )
    assert response.status_code == 200
    return response.json()


def test_get_watch_user_by_followed_user(created_watch_user):
    followed_user_id = created_watch_user['followed_user_id']  # 2
    response = client.get(
        f"/followed_user/{followed_user_id}/watchlist/",
        headers=headers_followed
    )
    response_data = response.json()
    assert created_watch_user in response_data


def test_get_watch_user_by_following_user(created_watch_user):
    following_user_id = created_watch_user['following_user_id']  # 3
    response = client.get(
        f"/following_user/{following_user_id}/watchlist/",
        headers=headers_following
    )
    response_data = response.json()
    assert created_watch_user in response_data


def test_get_watch_user_by_id(created_watch_user):
    following_user_id = created_watch_user['following_user_id']  # 3
    watch_user_id = created_watch_user['id']
    response = client.get(
        f"/following_user/{following_user_id}/watchlist/{watch_user_id}/",
        headers=headers_following
    )
    response_data = response.json()
    assert response_data == created_watch_user
