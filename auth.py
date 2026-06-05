import sqlite3

conn = sqlite3.connect("showroom.db", check_same_thread=False)
cursor = conn.cursor()

def create_default_users():
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("admin", "admin123", "admin"),
            ("sales", "sales123", "sales")
        ]
        cursor.executemany(
            "INSERT INTO users (username, password, role) VALUES (?,?,?)",
            users
        )
        conn.commit()


def login(username, password):
    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    return result[0] if result else None