"""
Database connection and utility functions
"""
import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """
    Create and return a database connection
    Returns: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=True  # Enable autocommit for immediate changes
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_db_connection(connection):
    """
    Close the database connection
    Args: connection - MySQL connection object
    """
    if connection and connection.is_connected():
        connection.close()

def execute_query(query, params=None, fetch=False):
    """
    Execute a database query with error handling
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (default: False)
    Returns: Query results if fetch=True, else None
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
            else:
                results = cursor.fetchone()
            cursor.close()
            close_db_connection(connection)
            return results
        else:
            cursor.close()
            close_db_connection(connection)
            return True
            
    except Error as e:
        print(f"Database error: {e}")
        cursor.close()
        close_db_connection(connection)
        return None