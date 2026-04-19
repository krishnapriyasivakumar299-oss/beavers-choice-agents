# seed_transactions.py
import sqlite3

conn = sqlite3.connect("munder_difflin.db")
cursor = conn.cursor()

# Clear existing rows (optional, so you don't duplicate)
cursor.execute("DELETE FROM transactions")

# Insert 19 demo rows
rows = [
    ("1", "stock_orders", 200, "2026-04-01"),
    ("1", "sales", 50, "2026-04-02"),
    ("2", "stock_orders", 500, "2026-04-03"),
    ("2", "sales", 100, "2026-04-04"),
    ("3", "stock_orders", 1000, "2026-04-05"),
    ("3", "sales", 200, "2026-04-06"),
    ("4", "stock_orders", 300, "2026-04-07"),
    ("4", "sales", 50, "2026-04-08"),
    ("5", "stock_orders", 400, "2026-04-09"),
    ("5", "sales", 100, "2026-04-10"),
    ("6", "stock_orders", 600, "2026-04-11"),
    ("6", "sales", 150, "2026-04-12"),
    ("7", "stock_orders", 800, "2026-04-13"),
    ("7", "sales", 200, "2026-04-14"),
    ("8", "stock_orders", 1000, "2026-04-15"),
    ("8", "sales", 250, "2026-04-16"),
    ("9", "stock_orders", 1200, "2026-04-17"),
    ("9", "sales", 300, "2026-04-18"),
    ("10", "stock_orders", 1500, "2026-04-19"),
]

cursor.executemany(
    "INSERT INTO transactions (item_name, transaction_type, units, transaction_date) VALUES (?, ?, ?, ?)",
    rows
)

conn.commit()
conn.close()

print("Inserted 19 rows into transactions table in munder_difflin.db")