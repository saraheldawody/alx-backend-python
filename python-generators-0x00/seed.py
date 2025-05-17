#!/usr/bin/env python3
import mysql.connector
import csv


def connect_db():
    """
    Connect to the MySQL server (no specific database).
    Returns a connection object or None on failure.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',       # adjust as needed
            password=''        # adjust as needed
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None


def create_database(connection):
    """
    Create the ALX_prodev database if it does not exist.
    """
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()


def connect_to_prodev():
    """
    Connect specifically to the ALX_prodev database.
    Returns a connection object or None on failure.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',       # adjust as needed
            password='',       # adjust as needed
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


def create_table(connection):
    """
    Create the user_data table if it does not exist.
    Fields:
      - user_id (VARCHAR(36) PRIMARY KEY)
      - name (VARCHAR(255) NOT NULL)
      - email (VARCHAR(255) NOT NULL)
      - age (DECIMAL NOT NULL)
    """
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX idx_user_id (user_id)
        );
        """
    )
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()


def insert_data(connection, data_file):
    """
    Insert rows from the given CSV file into user_data table.
    Uses INSERT IGNORE to skip duplicates.
    """
    cursor = connection.cursor()
    with open(data_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute(
                    """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (row['user_id'], row['name'], row['email'], row['age'])
                )
            except mysql.connector.Error as err:
                print(f"Error inserting row {row}: {err}")
    connection.commit()
    cursor.close()


def stream_user_data(connection):
    """
    Generator that yields each row from the user_data table one by one.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    for record in cursor:
        yield record
    cursor.close()
