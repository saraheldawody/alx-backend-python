import seed


def lazy_paginate(page_size):
    """
    Generator that yields pages of user rows lazily.
    Uses paginate_users to fetch each page on demand.
    Only one loop internally.
    """
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    Returns a list of dicts.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows