import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

PRIVATE_USER_FIELDS = {
    "birthday", "email", "tel_number", "street", "house_number", "zip_code",
    "city_town_village", "country", "notification"
}


def assert_public_user_contract(user_data: dict):
    """Assert that a public response contains no private account fields."""
    assert PRIVATE_USER_FIELDS.isdisjoint(user_data)
    assert set(user_data) == {
        "id", "first_name", "last_name", "username", "profile_picture_path",
        "commercial_account", "created_at", "account_status"
    }


def get_access_token(username: str, password: str):
    """
    Obtain an access token for a given username and password.
    """
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def create_user(username: str, password: str):
    """
    Create a new user or return the existing user data if the user already exists.
    """
    response_username = client.get(f"/users/username/{username}/")
    if response_username.status_code == 200:
        response_data = response_username.json()
        access_token = get_access_token(username, password)
        headers = {"Authorization": f"Bearer {access_token}"}
        return {"user_data": response_data, "headers": headers}
    response = client.post(
                           url="/users/",
                           data={
                                      "first_name": username,
                                      "last_name": username,
                                      "birthday": "2024-09-03",
                                      "username": username,
                                      "email": username + "@example.com",
                                      "tel_number": username,
                                      "street": username,
                                      "house_number": username,
                                      "zip_code": username,
                                      "city_town_village": username,
                                      "country": username,
                                      "commercial_account": "false",
                                      "notification": "true",
                                      "account_status": "true",
                                      "password": password
                                    }
                           )
    print(response.json())
    assert response.status_code == 200
    response_data = response.json()
    access_token = get_access_token(username, password)
    headers = {"Authorization": f"Bearer {access_token}"}
    return {"user_data": response_data, "headers": headers}


@pytest.fixture
def get_user_test():
    """
    Fixture for creating a test user and providing authentication headers.
    """
    username = "test1234"
    password = "test1234"
    return create_user(username=username, password=password)


def test_get_user(get_user_test: dict):
    """
    Test case for retrieving a public user profile without private fields.
    """
    headers = get_user_test['headers']
    user_id = get_user_test['user_data']['id']
    response = client.get(
        f"/users/{user_id}/",
        headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()
    assert_public_user_contract(response_data)
    assert response_data["id"] == user_id
    assert response_data["username"] == "test1234"


def test_public_user_list_and_username_lookup_hide_private_fields(get_user_test: dict):
    """Keep both other public user response paths on the reduced contract."""
    user_id = get_user_test["user_data"]["id"]

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    listed_user = next(user for user in list_response.json() if user["id"] == user_id)
    assert_public_user_contract(listed_user)

    username_response = client.get("/users/username/test1234/")
    assert username_response.status_code == 200
    assert_public_user_contract(username_response.json())


def test_current_user_keeps_private_account_fields(get_user_test: dict):
    """An authenticated user can still retrieve their own complete account data."""
    response = client.get("/users/me", headers=get_user_test["headers"])
    assert response.status_code == 200
    assert PRIVATE_USER_FIELDS.issubset(response.json())


def test_failing_update_user(get_user_test: dict):
    """
    Test case for attempting to update a user with incorrect authentication.
    """
    headers = get_user_test['headers']
    user_id = int(get_user_test['user_data']['id']) + 1
    response = client.put(
        f"/users/{user_id}/",
        json={
            "birthday": "2024-09-03",
            "username": "test1234",
            "email": "test1234@example.com",
            "tel_number": "test1234",
            "street": "test1234",
            "house_number": "test1234",
            "zip_code": "test1234"
        },
        headers=headers
    )
    assert response.status_code == 401
    assert response.json() == {
      "detail": "Authentication failed"
    }


def test_update_user(get_user_test: dict):
    """
    Test case for successfully updating user details.
    """
    headers = get_user_test['headers']
    user_id = get_user_test['user_data']['id']
    response = client.put(
        f"/users/{user_id}/",
        json={
          "birthday": "2024-09-03",
          "username": "test1234",
          "email": "test1234@example.com",
          "tel_number": "test1234",
          "street": "test1234",
          "house_number": "test1234",
          "zip_code": "test1234"
        },
        headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()
    response_data.pop("created_at", None)
    assert response_data == {
        "first_name": "test1234",
        "last_name": "test1234",
        "birthday": "2024-09-03",
        "username": "test1234",
        "email": "test1234@example.com",
        "tel_number": "test1234",
        "street": "test1234",
        "house_number": "test1234",
        "zip_code": "test1234",
        "city_town_village": "test1234",
        "country": "test1234",
        "commercial_account": False,
        "notification": True,
        "account_status": True,
        "id": user_id,
        "profile_picture_path": "https://buysellusers.s3.eu-north-1.amazonaws.com/019199fa-8037-7d"
                                "70-889d-e5738feb4bd7_28_08_2024_19_13_36_default_profile_pic.jpg"
    }
