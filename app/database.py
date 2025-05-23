import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """
)

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS categories (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """
)

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        in_stock INTEGER NOT NULL,
        category_id TEXT NOT NULL,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    """
)

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS clients (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        tel TEXT,
        email TEXT,
        address TEXT
    )
    """
)

conn.commit()

def get_db():
    return conn
