# Bestellzettel – Restaurant Order System

A lightweight, self-hosted restaurant order management system built for real-world use.

This project was developed with a focus on **clarity, simplicity, and control** rather than complexity.  
It is designed to be usable on phones and tablets by waiters, and easily extendable in the future
(kitchen view, reporting, inventory, etc.).

---

## Features

- Table-based ordering
- One active order per table
- Add / remove items with quantity tracking
- Automatic order creation on first item
- Order lifecycle:
  - `open`
  - `preparing`
  - `ready`
  - `closed` (paid)
  - `cancelled` (no bill / aborted)
- Real-time total price calculation
- Mobile-friendly waiter UI (works in browser)
- PostgreSQL-backed persistence
- Fully containerized with Docker
- Basic test suite with pytest

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Frontend:** Plain HTML + JavaScript
- **Containerization:** Docker + Docker Compose
- **Dependency Management:** Poetry
- **Testing:** pytest + TestClient

---

## Project Structure
```
├── src
│   └── bestellzettel
│       ├── static
│       │   ├── waiter.html
│       │   └── waiter.js
│       ├── routers
│       │   ├── __init__.py
│       │   ├── tables.py
│       │   ├── menu.py
│       │   └── orders.py
│       ├── __init__.py
│       ├── database.py
│       └── main.py
├── scripts
│   ├── data
│   │   ├── menu.csv
│   │   └── tables.csv
│   ├── sync_menu.py
│   └── sync_tables.py
├── docker
│   └── postgres
│       ├── schema.sql
│       ├── seed.sql
│       ├── 001_schema.sql
│       └── 002_seed.sql
```

---

## Running with Docker (Recommended)

### Prerequisites
- Docker
- Docker Compose (plugin or legacy)

### Start the app

```bash
docker compose up --build
```

This will start:

PostgreSQL database

FastAPI backend

### Access the app

Waiter UI:
http://localhost:8000/static/waiter.html

The app is accessible from other devices on the same network (e.g. phones).

### Database Initialization

Database schema and seed data are automatically applied using:

```bash
docker/postgres/001_schema.sql
docker/postgres/002_seed.sql
```

These files are mounted into the PostgreSQL container and executed on first startup.

### Menu & Table Sync

Menu items and tables can be managed via CSV files:


- ```data/menu.csv```
- ```data/tables.csv```

Sync scripts:
```bash
python data/scripts/sync_menu.py
python data/scripts/sync_tables.py
```

(These can later be automated or replaced with external tools like Google Sheets.)

### Tests

Run tests locally:

```bash
pytest
```

Tests use a dedicated test database and clean state via fixtures.

### Philosophy

This project intentionally avoids:

- Over-engineering

- Premature abstractions

- Heavy frontend frameworks

The goal is a clear, understandable system that can evolve based on real usage.

License

MIT
