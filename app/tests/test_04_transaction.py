import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_00_user import get_user_test
from app.tests.test_01_post import create_post
from app.tests.test_03_message import get_user_1234


client = TestClient(app)


@pytest.fixture
def get_user_seller(get_user_test):
    """
    Fixture for obtaining the seller user data.
    """
    return get_user_test


@pytest.fixture
def get_user_buyer(get_user_1234):
    """
    Fixture for obtaining the buyer user data.
    """
    return get_user_1234


@pytest.fixture
def create_transaction(create_post: dict, get_user_buyer: dict):
    """
    Fixture for creating a transaction between a buyer and a post.
    """
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


def test_get_transaction(create_transaction: dict, get_user_buyer: dict, get_user_seller: dict):
    """
    Test case for retrieving and verifying transaction details from both buyer's and seller's perspectives.
    """
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
    response = client.get(f"/users/{seller_id}/post/{post_id}/transaction/",
                          headers=headers_seller)
    assert response.status_code == 200
    seller_response_data_post_id = response.json()
    response = client.get(f"/users/{seller_id}/transaction/{transaction_id}/",
                          headers=headers_seller)
    assert response.status_code == 200
    response_seller_trans_id = response.json()
    response = client.get(f"/users/{seller_id}/received_transaction/",
                          headers=headers_seller)
    assert response.status_code == 200
    response_get_received_trans = response.json()

    assert buyer_response_data_post_id == seller_response_data_post_id
    assert response_buyer_trans_id == response_seller_trans_id
    for response in buyer_response_data_post_id:
        assert response == response_buyer_trans_id
    assert response_get_send_trans == response_get_received_trans


def test_failed_update_transaction(create_transaction: dict, get_user_buyer: dict):
    """
    Test case for attempting to update a transaction with various invalid and valid inputs.
    """
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
