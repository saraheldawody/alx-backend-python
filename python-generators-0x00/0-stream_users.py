#!/usr/bin/env python3

"""
0-stream_users.py

Generator for streaming rows from the user_data table one by one.
"""
import mysql.connector
from seed import connect_to_prodev


def stream_users():
    """
    Connect to the ALX_prodev database and yield each user row as a dict.
    Uses a single loop over the cursor as a generator.
    """
    conn = connect_to_prodev()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()
    conn.close()
