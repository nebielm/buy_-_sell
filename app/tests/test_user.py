import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def get_access_token():
    username = "test1234"
    password = "test1234"
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


access_token = get_access_token()
headers = {"Authorization": f"Bearer {access_token}"}


def test_get_user():
    user_id = 2
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
      "email": "user@example.com",
      "tel_number": "test1234",
      "street": "test1234",
      "house_number": "test1234",
      "zip_code": "test1234",
      "city_town_village": "test1234",
      "country": "test1234",
      "commercial_account": False,
      "notification": True,
      "account_status": True,
      "id": 2,
      "profile_picture_path": "https://buysellusers.s3.eu-north-1.amazonaws.com/019199fa-8037-7d70-889d-e5738feb4bd7"
                              "_28_08_2024_19_13_36_default_profile_pic.jpg"
    }


def test_failing_update_user():
    user_id = 3
    response = client.put(
        f"/users/{user_id}/",
        json={
            "birthday": "2024-09-03",
            "username": "test1234",
            "email": "user@example.com",
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


def test_update_user():
    user_id = 2
    response = client.put(
        f"/users/{user_id}/",
        json={
          "birthday": "2024-09-03",
          "username": "test1234",
          "email": "user@example.com",
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
        "email": "user@example.com",
        "tel_number": "test1234",
        "street": "test1234",
        "house_number": "test1234",
        "zip_code": "test1234",
        "city_town_village": "test1234",
        "country": "test1234",
        "commercial_account": False,
        "notification": True,
        "account_status": True,
        "id": 2,
        "profile_picture_path": "https://buysellusers.s3.eu-north-1.amazonaws.com/019199fa-8037-7d70-889d-e5738feb4bd7"
                                "_28_08_2024_19_13_36_default_profile_pic.jpg"
    }
