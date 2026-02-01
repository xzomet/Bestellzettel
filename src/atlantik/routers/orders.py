from fastapi import APIRouter, HTTPException
from atlantik.database import get_db_cursor
from atlantik.routers.tables import get_table

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
def create_order(table_id: int):
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO orders (table_id, status)
            VALUES (%s, 'open')
            RETURNING id
            """,
            (table_id,),
        )
        order_id = cur.fetchone()["id"]
        return {"order_id": order_id}


@router.post("/items")
def add_item(
    table_id: int,
    menu_item_id: int,
    delta: int,
    order_id: int | None = None,
    notes: str | None = None,
):
    if delta == 0:
        raise HTTPException(status_code=400, detail="Delta cannot be 0")

    with get_db_cursor() as cur:
        if order_id is None:
            cur.execute(
                """
                SELECT id
                FROM orders
                WHERE table_id = %s AND status = 'open'
                """,
                (table_id,),
            )
            row = cur.fetchone()

            if row:
                order_id = row["id"]
            else:
                cur.execute(
                    """
                    INSERT INTO orders (table_id, status)
                    VALUES (%s, 'open')
                    RETURNING id
                    """,
                    (table_id,),
                )
                order_id = cur.fetchone()["id"]
        cur.execute(
            """
            UPDATE order_items
            SET quantity = quantity + %s
            WHERE order_id = %s AND menu_item_id = %s
            RETURNING quantity
            """,
            (delta, order_id, menu_item_id),
        )
        row = cur.fetchone()

        if row is None:
            if delta > 0:
                cur.execute(
                    """
                    INSERT INTO order_items (order_id, menu_item_id, quantity, notes)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order_id, menu_item_id, delta, notes),
                )
        else:
            if row["quantity"] <= 0:
                cur.execute(
                    """
                    DELETE FROM order_items
                    WHERE order_id = %s AND menu_item_id = %s
                    """,
                    (order_id, menu_item_id),
                )

    return {"status": "ok", "order_id": order_id}


@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: str):
    if status not in ("open", "preparing", "ready", "closed", "cancelled"):
        raise HTTPException(status_code=400, detail="Invalid status")

    with get_db_cursor() as cur:
        cur.execute(
            """
            UPDATE orders
            SET status = %s
            WHERE id = %s
            RETURNING id, status
            """,
            (status, order_id),
        )
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

    return row


@router.post("/{order_id}/close")
def close_order(order_id: int):
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) AS item_count
            FROM order_items
            WHERE order_id = %s
            """,
            (order_id,),
        )
        item_count = cur.fetchone()["item_count"]

        new_status = "cancelled" if item_count == 0 else "closed"

        cur.execute(
            """
            UPDATE orders
            SET status = %s
            WHERE id = %s
                AND status NOT IN ('closed', 'cancelled')
            RETURNING id, status
            """,
            (
                new_status,
                order_id,
            ),
        )
        row = cur.fetchone()

        if row is None:
            raise HTTPException(
                status_code=400,
                detail="Order already closed or does not exist",
            )

        return {
            "order_id": row["id"],
            "status": row["status"],
        }
