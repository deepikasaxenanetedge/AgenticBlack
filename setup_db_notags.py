from db_config import get_db_connection

def setup_database():
    db = get_db_connection()
    cursor = db.cursor()

    # Fix: Use backticks (`) around the column name since `condition` is a reserved keyword
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NO_TAGS (
            `condition` VARCHAR(255) NOT NULL PRIMARY KEY
        )
    """)

    rules = [
        ("NOtag1",),
        ("NOtag2",),
        ("NOtag3",),
        ("NOtag4",),
        ("NOtag1_tag2",),
        ("NOtag2_tag3",),
        ("NOtag3_tag4",),
    ]

    cursor.executemany("INSERT IGNORE INTO NO_TAGS (`condition`) VALUES (%s)", rules)

    db.commit()
    db.close()
    print("Database setup completed.")

if __name__ == "__main__":
    setup_database()
