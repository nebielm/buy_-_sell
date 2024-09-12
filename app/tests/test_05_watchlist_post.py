import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import get_user_test
from app.tests.test_01_post import create_post
from app.tests.test_03_message import get_user_1234


client = TestClient(app)


@pytest.fixture
def get_post_user(get_user_test):
    """
    Fixture to obtain the user data who created the post.
    """
    return get_user_test


@pytest.fixture
def get_following_user(get_user_1234):
    """
    Fixture to obtain the data of a user who is following.
    """
    return get_user_1234


@pytest.fixture
def create_watch_post(create_post: dict, get_following_user: dict):
    """
    Fixture to create a watch post-entry for a user.
    """
    user_id = get_following_user['user_data']["id"]
    headers = get_following_user['headers']
    post_id = create_post['id']
    response = client.post(
        f"/user/{user_id}/watchlist/post/{post_id}/",
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


def test_get_watch_posts_by_followed_post(create_watch_post: dict, get_post_user: dict):
    """
    Test case to verify that a watched post can be retrieved by the user who created it.
    """
    user_id = get_post_user['user_data']['id']
    post_headers = get_post_user['headers']
    post_id = create_watch_post['followed_post_id']
    response = client.get(
        f"/user/{user_id}/watchlist/post/{post_id}/",
        headers=post_headers
    )
    response_data = response.json()
    assert create_watch_post in response_data


def test_get_watch_posts_by_following_user(create_watch_post: dict, get_following_user: dict):
    """
    Test case to verify that a user can retrieve their watchlist of posts.
    """
    user_id = get_following_user['user_data']["id"]
    headers = get_following_user['headers']
    response = client.get(
        f"/user/{user_id}/watchlist/",
        headers=headers
    )
    response_data = response.json()
    assert create_watch_post in response_data


def test_get_watch_posts_by_id(create_watch_post: dict, get_following_user: dict):
    """
    Test case to verify that a user can retrieve a specific watched post by its ID.
    """
    user_id = get_following_user['user_data']["id"]
    headers = get_following_user['headers']
    watch_post_id = create_watch_post['id']
    response = client.get(
        f"/user/{user_id}/watchlist/{watch_post_id}/",
        headers=headers
    )
    response_data = response.json()
    assert create_watch_post == response_data
