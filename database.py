import mysql.connector

def create_connection():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=3306
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:",err)
        return None

def create_database():
    conn=create_connection()

    if conn is None:
        return

    cursor=conn.cursor()

    cursor.execute("create database if not exists expense_tracker")
    cursor.execute("use expense_tracker")

    cursor.execute("""
        create table if not exists transactions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(20) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            category VARCHAR(50) NOT NULL,
            description VARCHAR(255),
            transaction_date DATE NOT NULL
        )
    """)

    print("Expense Tracker database is ready!")

    cursor.close()
    conn.close()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="expense_tracker",
        port=3306
    )
