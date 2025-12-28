"""
Script to reset the database - drops all tables and recreates them
Run this if you get "table already exists" errors
"""
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '',
    'database': 'docdrop_db'
}

def reset_database():
    try:
        print("Connecting to MySQL...")
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        
        print("Dropping database...")
        cursor.execute("DROP DATABASE IF EXISTS docdrop_db")
        
        print("Creating database...")
        cursor.execute("CREATE DATABASE docdrop_db")
        
        cursor.close()
        connection.close()
        
        print("[SUCCESS] Database reset complete!")
        print("Now run: python manage.py migrate")
        
    except Error as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    reset_database()


