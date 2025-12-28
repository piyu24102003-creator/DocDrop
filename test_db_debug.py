import socket
import pymysql

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def check_db_connection(host, port, user, password, db_name):
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
        print(f"Successfully connected to MySQL on port {port}")
        
        # Check if database exists
        cursor = conn.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        if cursor.fetchone():
            print(f"Database '{db_name}' exists.")
        else:
            print(f"Database '{db_name}' does NOT exist. Attempting to create...")
            try:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created successfully.")
            except Exception as e:
                print(f"Failed to create database: {e}")
        conn.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Failed to connect to MySQL on port {port}: {e}")
        return False

print("Checking ports...")
ports = [3306, 3307]
for port in ports:
    is_open = check_port('127.0.0.1', port)
    status = "OPEN" if is_open else "CLOSED"
    print(f"Port {port}: {status}")
    
    if is_open:
        check_db_connection('127.0.0.1', port, 'root', '', 'docdrop_db')
