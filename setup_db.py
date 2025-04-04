from db_config import get_db_connection

def setup_database():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_source (
            id INT AUTO_INCREMENT PRIMARY KEY,
            condition VARCHAR(255) UNIQUE NOT NULL,
            action VARCHAR(255) NOT NULL
        )
    """)

    rules = [
        ("tag1", "action1"),
        ("tag2", "action2"),
        ("tag3", "action3"),
        ("tag4", "action4"),
        ("tag1_tag2", "action5"),
        ("tag2_tag3", "action6"),
        ("tag3_tag4", "action7"),
    ]

    cursor.executemany("INSERT IGNORE INTO knowledge_source (condition, action) VALUES (%s, %s)", rules)
    db.commit()
    db.close()
    print("Database setup completed.")

if __name__ == "__main__":
    setup_database()
