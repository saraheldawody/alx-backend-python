import sqlite3
class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params if params is not None else ()
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def execute(self):
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        return cursor.fetchall()
    
# Using the ExecuteQuery context manager to execute a query
def fetch_users_by_age(age):
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(query, (age,)) as executor:
        return executor.execute()
    
# Fetch users older than 25 using the ExecuteQuery context manager
users = fetch_users_by_age(25)
print(users)

