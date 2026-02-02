import csv
import os

from tischapp.database import get_db_cursor

TABLES_FILE = "data/tables.csv"


def sync_tables():
    # Check if CSV file exists
    if not os.path.exists(TABLES_FILE):
        print(f"⚠️  Tables CSV file not found: {TABLES_FILE}")
        return

    with open(TABLES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tables = list(reader)

    with get_db_cursor() as cur:
        # Load existing tables
        cur.execute("SELECT id, name, is_active FROM tables")
        existing = {row["name"]: row for row in cur.fetchall()}

        seen_names = set()

        for table in tables:
            name = table["name"].strip()
            is_active = table.get("is_active", "true").lower() == "true"

            seen_names.add(name)

            if name in existing:
                # Update only if is_active has changed
                if existing[name]["is_active"] != is_active:
                    cur.execute(
                        """
                        UPDATE tables
                        SET is_active = %s
                        WHERE name = %s
                        """,
                        (is_active, name),
                    )
                    print(f"📝 Updated table: {name} (active: {is_active})")
            else:
                cur.execute(
                    """
                    INSERT INTO tables (name, is_active)
                    VALUES (%s, %s)
                    """,
                    (name, is_active),
                )
                print(f"➕ Added new table: {name} (active: {is_active})")

        # Deactivate tables not in CSV
        for name, table_info in existing.items():
            if name not in seen_names:
                if table_info["is_active"]:  # Only update if currently active
                    cur.execute(
                        """
                        UPDATE tables
                        SET is_active = false
                        WHERE name = %s
                        """,
                        (name,),
                    )
                    print(f"📝 Deactivated missing table: {name}")


if __name__ == "__main__":
    sync_tables()
    print("✅ Tables synced successfully.")
