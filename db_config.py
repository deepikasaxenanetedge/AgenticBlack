import mysql.connector

def get_db_connection():
    """Establish connection to intelligent_agent_db database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="intelligent_agent_db"
    )
