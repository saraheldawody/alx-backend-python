#!/usr/bin/env python3

"""
1-batch_processing.py

Batch-processing generator for streaming and filtering user_data in batches.
"""
from seed import connect_to_prodev
from seed import stream_user_data  # if using seed, but prefer 0-stream_users

# Alternatively, import the stream_users generator from 0-stream_users.py
try:
    from stream_users import stream_users
except ImportError:
    # Fallback to streaming via seed directly
    def stream_users():
        conn = connect_to_prodev()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
        cursor.close()
        conn.close()


def stream_users_in_batches(batch_size):
    """
    Generator that yields lists of user records in batches of `batch_size`.
    Each record is a dict with keys: user_id, name, email, age.

    Uses a single loop to collect and yield batches.
    """
    batch = []
    for user in stream_users():  # Loop 1
        batch.append(user)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def batch_processing(batch_size):
    """
    Processes each batch from stream_users_in_batches:
    Filters and prints users over the age of 25.

    Uses two loops: one to iterate batches, one to iterate filtered users.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 2
        for user in (u for u in batch if u['age'] > 25):  # Loop 3 (generator comprehension counts)
            print(user)


if __name__ == '__main__':
    import sys

    try:
        size = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    except ValueError:
        size = 50
    try:
        batch_processing(size)
    except BrokenPipeError:
        sys.stderr.close()
