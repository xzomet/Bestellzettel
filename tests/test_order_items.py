from fastapi.testclient import TestClient
from atlantik.main import app

client = TestClient(app)


def test_add_and_remove_item():
    # Get order
    r = client.get("/tables/1")

    if r.json()["order_status"] != "closed":
        order_id = r.json()["order_id"]
        client.post(f"/orders/{order_id}/close")

    # Add item
    r = client.post(
        "/orders/items",
        params={"table_id": 1, "menu_item_id": 1, "delta": 1},
    )
    assert r.status_code == 200

    # Verify quantity
    r = client.get("/tables/1")
    items = r.json()["order_items"]
    assert items[0]["quantity"] == 1

    # Remove item
    r = client.post(
        "/orders/items",
        params={"table_id": 1, "menu_item_id": 1, "delta": -1},
    )

    # Item should be gone
    r = client.get("/tables/1")
    items = r.json()["order_items"]
    print("asdas")
    assert items == []
