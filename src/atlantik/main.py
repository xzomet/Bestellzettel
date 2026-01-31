# main.py
from fastapi import FastAPI, HTTPException
from atlantik.database import get_db_cursor

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from atlantik.routers import orders, menu, tables

app = FastAPI(title="Restaurant Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for local network
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="src/atlantik/static"), name="static")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/debug")
async def debug():
    with get_db_cursor() as cur:
        cur.execute("SELECT current_user, current_database()")
        result = cur.fetchone()
        return {
            "user": result["current_user"],
            "database": result["current_database"],
            "is_superuser": "SELECT rolsuper FROM pg_roles WHERE rolname = current_user",
        }


app.include_router(orders.router)
app.include_router(tables.router)
app.include_router(menu.router)
