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
def get_user_seller():
    username = "test1234"
    password = "test1234"
    return create_user(username=username, password=password)


@pytest.fixture
def get_user_buyer():
    username = "1234test"
    password = "1234test"
    return create_user(username=username, password=password)


@pytest.fixture
def create_post(get_user_seller):
    headers_seller = get_user_seller["headers"]
    user_id = get_user_seller["user_data"]["id"]
    response = client.get(f"/users/{user_id}/posts/",
                          headers=headers_seller
                          )
    to_delete = response.json()
    if to_delete:
        for post in to_delete:
            post_id = post['id']
            client.delete(f"/posts/{post_id}/",
                          headers=headers_seller
                          )
    response = client.post(
        f"/users/{user_id}/posts/",
        json={
          "title": "test1234",
          "description": "test1234",
          "price": 2.0,
          "condition": "test1234",
          "quantity": 10,
          "status": "available",
          "user_id": user_id,
          "sub_category_id": 139
        },
        headers=headers_seller
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_transaction(create_post, get_user_buyer):
    user_id = get_user_buyer["user_data"]["id"]
    headers_buyer = get_user_buyer["headers"]
    post_id = create_post["id"]
    response = client.post(f"/users/{user_id}/post/{post_id}/transaction/",
                           json={"price": 10.0,
                                 "quantity": 5,
                                 "status": "in_progress"},
                           headers=headers_buyer)
    assert response.status_code == 200
    return response.json()


def test_get_transaction(create_transaction, get_user_buyer, get_user_seller):
    buyer_id = create_transaction["buyer_id"]
    headers_buyer = get_user_buyer["headers"]
    post_id = create_transaction["post_id"]
    transaction_id = create_transaction["id"]
    response = client.get(f"/users/{buyer_id}/post/{post_id}/transaction/", headers=headers_buyer)
    assert response.status_code == 200
    buyer_response_data_post_id = response.json()
    response = client.get(f"/users/{buyer_id}/transaction/{transaction_id}/", headers=headers_buyer)
    assert response.status_code == 200
    response_buyer_trans_id = response.json()
    response = client.get(f"/users/{buyer_id}/sent_transaction/", headers=headers_buyer)
    assert response.status_code == 200
    response_get_send_trans = response.json()

    seller_id = create_transaction["seller_id"]
    headers_seller = get_user_seller["headers"]
    response = client.get(f"/users/{seller_id}/post/{post_id}/transaction/", headers=headers_seller)
    assert response.status_code == 200
    seller_response_data_post_id = response.json()
    response = client.get(f"/users/{seller_id}/transaction/{transaction_id}/", headers=headers_seller)
    assert response.status_code == 200
    response_seller_trans_id = response.json()
    response = client.get(f"/users/{seller_id}/received_transaction/", headers=headers_seller)
    assert response.status_code == 200
    response_get_received_trans = response.json()

    assert buyer_response_data_post_id == seller_response_data_post_id
    assert response_buyer_trans_id == response_seller_trans_id
    for response in buyer_response_data_post_id:
        assert response == response_buyer_trans_id
    assert response_get_send_trans == response_get_received_trans


def test_failed_update_transaction(create_transaction, get_user_buyer):
    user_id = create_transaction["buyer_id"]
    headers_buyer = get_user_buyer["headers"]
    transaction_id = create_transaction["id"]
    response = client.put(f"/users/{user_id}/transaction/{transaction_id}/",
                          json={"price": 30.0, "quantity": 5},
                          headers=headers_buyer)
    assert response.status_code == 403
    response = client.put(f"/users/{user_id}/transaction/{transaction_id}/",
                          json={"price": 22.0, "quantity": 11},
                          headers=headers_buyer)
    assert response.status_code == 403
    response = client.put(f"/users/{user_id}/transaction/{transaction_id}/",
                          json={"price": 6.0, "quantity": 3},
                          headers=headers_buyer)
    assert response.status_code == 200
    response_data = response.json()
    response_data.pop("last_status_change")
    assert response_data == {
                              "price": 6,
                              "quantity": 3,
                              "status": "in_progress",
                              "id": create_transaction['id'],
                              "buyer_id": create_transaction['buyer_id'],
                              "seller_id": create_transaction['seller_id'],
                              "post_id": create_transaction['post_id']
                            }