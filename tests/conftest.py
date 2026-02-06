import pytest
from bestellzettel.database import get_db_cursor


@pytest.fixture(autouse=True)
def clean_db():
    """
    Ensures each test runs with a clean database state.
    """
    with get_db_cursor() as cur:
        # Order matters because of FK constraints
        cur.execute("DELETE FROM order_items")
        cur.execute("DELETE FROM orders")

        # Optional: reset tables to known state
        cur.execute("""
            INSERT INTO tables (id, name, is_active)
            VALUES
                (1, 'Table 1', true)
            ON CONFLICT (id) DO NOTHING
        """)

        cur.execute("""
            INSERT INTO menu_items (id, name, price_cents, is_active)
            VALUES
                (1, 'Test Dish', 1000, true)
            ON CONFLICT (id) DO NOTHING
        """)

    yield
