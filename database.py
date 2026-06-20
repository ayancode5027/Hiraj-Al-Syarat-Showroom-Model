import sqlite3

conn = sqlite3.connect("showroom.db", check_same_thread=False)
cursor = conn.cursor()

# ================= USERS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# ================= CARS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    year INTEGER,
    condition TEXT,
    purchase_price INTEGER,
    price INTEGER,
    engine TEXT,
    transmission TEXT,
    fuel_type TEXT,
    color TEXT,
    stock INTEGER,
    image_url TEXT,
    description TEXT
)
""")

# ================= BOOKINGS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    car TEXT,
    date TEXT,
    time TEXT
)
""")

# ================= LEADS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    car TEXT
)
""")

# ================= SALES TABLE =================
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

conn.commit()

# ================= SAMPLE DATA =================
cursor.execute("SELECT COUNT(*) FROM cars")

if cursor.fetchone()[0] == 0:

    sample_cars = [

        (
            "Toyota",
            "Camry",
            2025,
            "New",
            100000,     # purchase price
            120000,     # sale price
            "2.5L",
            "Automatic",
            "Petrol",
            "White",
            5,
            "https://example.com/camry.jpg",
            "Luxury family sedan"
        ),

        (
            "Hyundai",
            "Elantra",
            2024,
            "Used",
            70000,
            80000,
            "2.0L",
            "Automatic",
            "Petrol",
            "Black",
            3,
            "https://example.com/elantra.jpg",
            "Excellent condition"
        ),

        (
            "Kia",
            "K5",
            2025,
            "New",
            95000,
            110000,
            "2.5L",
            "Automatic",
            "Petrol",
            "Red",
            4,
            "https://example.com/k5.jpg",
            "Sport sedan"
        ),

        (
            "BMW",
            "X5",
            2025,
            "New",
            220000,
            250000,
            "3.0L",
            "Automatic",
            "Petrol",
            "White",
            2,
            "https://example.com/x5.jpg",
            "Luxury SUV"
        )

    ]

    cursor.executemany("""
    INSERT INTO cars (
        brand,
        model,
        year,
        condition,
        purchase_price,
        price,
        engine,
        transmission,
        fuel_type,
        color,
        stock,
        image_url,
        description
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, sample_cars)

    conn.commit()

