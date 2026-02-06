from fastapi import APIRouter
from bestellzettel.database import get_db_cursor

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("/")
def get_tables():
    with get_db_cursor() as cur:
        cur.execute("""
        SELECT
            t.id,
            t.name,
            CASE
                WHEN EXISTS (
                    SELECT 1 FROM orders o
                    WHERE o.table_id = t.id AND o.status = 'open'
                ) THEN 'open'
                ELSE 'available'
            END as order_status
        FROM tables t
        WHERE t.is_active = True
        ORDER BY t.id
        """)
        return {"tables": cur.fetchall()}


@router.get("/{table_id}")
def get_table(table_id):
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT id, status
            FROM orders
            WHERE table_id = %s and status = 'open'
            """,
            (table_id,),
        )
        order = cur.fetchone()

        if order is None:

            return {
                "table_id": table_id,
                "order_id": None,
                "order_status": "closed",
                "order_items": [],
                "total_price_cents": 0,
            }

        order_id = order["id"]
        order_status = order["status"]

        cur.execute(
            """
            SELECT
                oi.menu_item_id,
                oi.quantity,
                oi.price_cents,
                oi.notes
            FROM order_items oi
            WHERE oi.order_id = %s
            ORDER BY oi.created_at;
            """,
            (order_id,),
        )
        order_items = cur.fetchall()

        cur.execute(
            """
            SELECT
            COALESCE(SUM(oi.quantity * oi.price_cents), 0) AS total_price_cents
            FROM order_items oi
            JOIN menu_items mi ON mi.id = oi.menu_item_id
            WHERE oi.order_id = %s
            """,
            (order_id,),
        )
        total_price_cents = cur.fetchone()["total_price_cents"]
        return {
            "table_id": table_id,
            "order_id": order_id,
            "order_status": order_status,
            "order_items": order_items,
            "total_price_cents": total_price_cents,
        }
