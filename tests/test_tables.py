from fastapi.testclient import TestClient
from tischapp.main import app

client = TestClient(app)


def test_one_open_order_per_table():
    r1 = client.get("tables/1")
    assert r1.status_code == 200
    order_id_1 = r1.json()["order_id"]

    r2 = client.get("tables/1")
    assert r2.status_code == 200
    order_id_2 = r2.json()["order_id"]

    assert order_id_1 == order_id_2
