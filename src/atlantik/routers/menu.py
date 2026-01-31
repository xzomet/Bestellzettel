from fastapi import APIRouter, HTTPException
from atlantik.database import get_db_cursor

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/")
def get_menu():
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT id, name, price_cents
            FROM menu_items
            WHERE is_active = true
            ORDER BY id
            """)
        return {"menu": cur.fetchall()}
