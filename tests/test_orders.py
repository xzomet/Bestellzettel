from fastapi.testclient import TestClient
from atlantik.main import app

client = TestClient(app)


def test_add_item_creates_single_open_order():
    # Arrange
    table_id = 1
    menu_item_id = 1

    r = client.get("/tables/1")

    if r.json()["order_status"] != "closed":
        order_id = r.json()["order_id"]
        client.post(f"/orders/{order_id}/close")

    # Act 1: add first item (should create order)
    r1 = client.post(
        "/orders/items",
        params={
            "table_id": table_id,
            "menu_item_id": menu_item_id,
            "delta": 1,
        },
    )
    assert r1.status_code == 200
    order_id_1 = r1.json()["order_id"]

    # Act 2: add second item WITHOUT passing order_id
    r2 = client.post(
        "/orders/items",
        params={
            "table_id": table_id,
            "menu_item_id": menu_item_id,
            "delta": 1,
        },
    )
    assert r2.status_code == 200
    order_id_2 = r2.json()["order_id"]

    # Assert: same order reused
    assert order_id_1 == order_id_2
