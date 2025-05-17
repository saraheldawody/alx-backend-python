from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields each user's age from the user_data table one by one.
    """
    conn = connect_to_prodev()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()


def compute_average_age():
    """
    Computes and prints the average age of all users without loading them into memory.
    Uses one loop over the age generator.
    """
    total = 0.0
    count = 0
    for age in stream_user_ages():  # Loop 1: aggregation
        total += float(age)
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average}")


if __name__ == '__main__':
    compute_average_age()
