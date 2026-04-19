# init_db.py
from sqlalchemy import create_engine, text

# IMPORTANT: match the same DB file used in project_starter.py
engine = create_engine("sqlite:///munder_difflin.db")

with engine.connect() as conn:
    # Create transactions table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            transaction_type TEXT NOT NULL,  -- 'stock_orders' or 'sales'
            units INTEGER NOT NULL,
            transaction_date TEXT NOT NULL
        )
    """))

    # Create quote_requests table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS quote_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            response TEXT
        )
    """))

    # Create quotes table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            total_amount REAL,
            quote_explanation TEXT,
            job_type TEXT,
            order_size TEXT,
            event_type TEXT,
            order_date TEXT,
            FOREIGN KEY(request_id) REFERENCES quote_requests(id)
        )
    """))

    conn.commit()

print("Tables created successfully in munder_difflin.db")