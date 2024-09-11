import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def get_access_token(username, password):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def create_user(username, password):
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
    username = "test1234"
    password = "test1234"
    return create_user(username=username, password=password)


def test_get_user(get_user_test):
    headers = get_user_test['headers']
    user_id = get_user_test['user_data']['id']
    response = client.get(
        f"/users/{user_id}/",
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
      "profile_picture_path": "https://buysellusers.s3.eu-north-1.amazonaws.com/019199fa-8037-7d70"
                              "-889d-e5738feb4bd7_28_08_2024_19_13_36_default_profile_pic.jpg"
    }


def test_failing_update_user(get_user_test):
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


def test_update_user(get_user_test):
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
