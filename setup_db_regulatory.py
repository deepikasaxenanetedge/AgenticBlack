from db_config import get_db_connection

def setup_database():
    db = get_db_connection()
    cursor = db.cursor()

    # Fix: Enclose `condition` in backticks (`) to prevent syntax issues
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regulatory_rules (
            `condition` VARCHAR(255) PRIMARY KEY,
            action VARCHAR(255) NOT NULL
        )
    """)

    rules = [
        ("Rtag1", "action1"),
        ("Rtag2", "action2"),
        ("Rtag3", "action3"),
        ("Rtag4", "action4"),
    ]

    # Fix: Ensure `condition` is enclosed in backticks in the INSERT statement as well
    cursor.executemany("INSERT IGNORE INTO regulatory_rules (`condition`, action) VALUES (%s, %s)", rules)

    db.commit()
    db.close()
    print("Database setup completed.")

if __name__ == "__main__":
    setup_database()

