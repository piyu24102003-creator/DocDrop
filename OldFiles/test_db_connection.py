"""
Quick script to test MySQL connection
Run this to verify your database connection before running migrations
"""
import mysql.connector
from mysql.connector import Error

# Database configuration - update if needed
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '',  # Change this if you have a MySQL password
    'database': 'docdrop_db'
}

def test_connection():
    """Test MySQL connection"""
    try:
        print("Testing MySQL connection...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"User: {DB_CONFIG['user']}")
        print(f"Password: {'(set)' if DB_CONFIG['password'] else '(empty)'}")
        print(f"Database: {DB_CONFIG['database']}")
        print("-" * 50)
        
        # Try to connect
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            print("[SUCCESS] Successfully connected to MySQL!")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'docdrop_db'")
            result = cursor.fetchone()
            
            if result:
                print("[SUCCESS] Database 'docdrop_db' exists!")
            else:
                print("[WARNING] Database 'docdrop_db' does NOT exist.")
                print("Creating database...")
                cursor.execute("CREATE DATABASE docdrop_db")
                print("[SUCCESS] Database 'docdrop_db' created!")
            
            cursor.close()
            connection.close()
            print("\n[SUCCESS] Connection test passed! You can now run migrations.")
            return True
            
    except Error as e:
        print(f"\n[ERROR] Connection failed!")
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure XAMPP MySQL is running")
        print("2. Check if you have a MySQL password set")
        print("3. If you have a password, update PASSWORD in this script and settings.py")
        print("4. Verify MySQL is listening on port 3306")
        return False

if __name__ == "__main__":
    test_connection()

