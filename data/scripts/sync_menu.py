import csv

from atlantik.database import get_db_cursor

MENU_FILE = "../../data/menu.csv"


def sync_menu():
    with open(MENU_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        menu_items = list(reader)

    with get_db_cursor() as cur:
        # Load existing items
        cur.execute("SELECT id, name FROM menu_items")
        existing = {row["name"]: row["id"] for row in cur.fetchall()}

        seen_names = set()

        for item in menu_items:
            name = item["name"].strip()
            price = int(item["price_cents"])
            is_active = item["is_active"].lower() == "true"

            seen_names.add(name)

            if name in existing:
                cur.execute(
                    """
                    UPDATE menu_items
                    SET price_cents = %s, is_active = %s
                    WHERE name = %s
                    """,
                    (price, is_active, name),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO menu_items (name, price_cents, is_active)
                    VALUES (%s, %s, %s)
                    """,
                    (name, price, is_active),
                )

        for name in existing:
            if name not in seen_names:
                cur.execute(
                    """
                    UPDATE menu_items
                    SET is_active = false
                    WHERE name = %s
                    """,
                    (name,),
                )


if __name__ == "__main__":
    sync_menu()
    print("Menu synced.")
