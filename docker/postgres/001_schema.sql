-- =========================
-- BESTELLZETTEBESTELLZETTEL FRESH SCHEMA
-- =========================

-- Development only
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS menu_items CASCADE;
DROP TABLE IF EXISTS tables CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =========================
-- USERS (future use)
-- =========================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL CHECK (role IN ('admin', 'manager', 'waiter', 'chef')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =========================
-- TABLES (physical tables)
-- =========================
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT true
);

-- =========================
-- MENU ITEMS (catalog)
-- =========================
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL DEFAULT 'other',
    name TEXT NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_id INTEGER NOT NULL REFERENCES tables(id),
    status TEXT NOT NULL CHECK (
        status IN ('open', 'preparing', 'ready', 'closed', 'cancelled')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at TIMESTAMPTZ
);

-- Exactly one open order per table
CREATE UNIQUE INDEX one_open_order_per_table
ON orders (table_id)
WHERE status = 'open';

-- =========================
-- ORDER ITEMS (line items)
-- =========================
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,

    order_id INTEGER NOT NULL
        REFERENCES orders(id) ON DELETE CASCADE,

    menu_item_id INTEGER NOT NULL
        REFERENCES menu_items(id),

    quantity INTEGER NOT NULL CHECK (quantity > 0),

    -- SNAPSHOT PRICE (critical)
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),

    -- Price override metadata
    price_override_reason TEXT,
    price_overridden_at TIMESTAMPTZ,

    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Prevent duplicate menu items per order
CREATE UNIQUE INDEX unique_order_item
ON order_items (order_id, menu_item_id);
