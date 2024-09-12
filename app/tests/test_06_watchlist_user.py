import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import get_user_test
from app.tests.test_03_message import get_user_1234

client = TestClient(app)


@pytest.fixture
def get_following_user(get_user_test):
    """
    Fixture to obtain the user data of the user who is following.
    """
    return get_user_test


@pytest.fixture
def get_followed_user(get_user_1234):
    """
    Fixture to obtain the user data of the user being followed.
    """
    return get_user_1234


@pytest.fixture
def created_watch_user(get_following_user: dict, get_followed_user: dict):
    """
    Fixture to create a watch user entry in the following user's watchlist.
    """
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


def test_get_watch_user_by_followed_user(created_watch_user: dict, get_followed_user: dict):
    """
    Test case to verify that a watched user can be retrieved by the user being followed.
    """
    followed_user_id = created_watch_user['followed_user_id']
    headers_followed = get_followed_user['headers']
    response = client.get(
        f"/followed_user/{followed_user_id}/watchlist/",
        headers=headers_followed
    )
    response_data = response.json()
    assert created_watch_user in response_data


def test_get_watch_user_by_following_user(created_watch_user: dict, get_following_user: dict):
    """
    Test case to verify that a watched user can be retrieved by the user who follows.
    """
    following_user_id = created_watch_user['following_user_id']
    headers_following = get_following_user['headers']
    response = client.get(
        f"/following_user/{following_user_id}/watchlist/",
        headers=headers_following
    )
    response_data = response.json()
    assert created_watch_user in response_data


def test_get_watch_user_by_id(created_watch_user: dict, get_following_user: dict):
    """
    Test case to verify that a specific watched user can be retrieved by its ID.
    """
    following_user_id = created_watch_user['following_user_id']
    headers_following = get_following_user['headers']
    watch_user_id = created_watch_user['id']
    response = client.get(
        f"/following_user/{following_user_id}/watchlist/{watch_user_id}/",
        headers=headers_following
    )
    response_data = response.json()
    assert response_data == created_watch_user
