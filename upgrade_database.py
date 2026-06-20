import sqlite3

conn = sqlite3.connect("showroom.db")
cursor = conn.cursor()

# Add purchase_price column if it doesn't exist
try:
    cursor.execute("""
    ALTER TABLE cars
    ADD COLUMN purchase_price INTEGER DEFAULT 0
    """)
    print("purchase_price column added")
except:
    print("purchase_price column already exists")

# Create sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER,
    brand TEXT,
    model TEXT,
    purchase_price REAL,
    sale_price REAL,
    customer_name TEXT,
    customer_phone TEXT,
    sale_date TEXT,
    profit REAL
)
""")

print("sales table ready")

conn.commit()
conn.close()

print("Database upgraded successfully")

