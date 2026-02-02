from fastapi import APIRouter, HTTPException
from tischapp.database import get_db_cursor

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/")
def get_menu():
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT category, id, name, price_cents
            FROM menu_items
            WHERE is_active = true
            ORDER BY category, name
            """)
        return {"menu": cur.fetchall()}
