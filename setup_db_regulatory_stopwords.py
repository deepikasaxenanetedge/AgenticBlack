from db_config import get_db_connection

def setup_database():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regulatory_stopwords (
            words VARCHAR(255) PRIMARY KEY
        )
    """)

    # Fix: Convert rules to a list of single-element tuples
    rules = [
        ("word1",),
        ("word2",),
        ("word3",),
        ("word4",)
    ]

    cursor.executemany("INSERT IGNORE INTO regulatory_stopwords (words) VALUES (%s)", rules)

    db.commit()
    db.close()
    print("Database setup completed.")

if __name__ == "__main__":
    setup_database()


