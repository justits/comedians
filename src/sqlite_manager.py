import sqlite3
import pandas as pd
import os


class SQLiteManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.create_connection()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Connected to SQLite database.")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    def create_table(self, table_name, schema):
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"
            self.conn.execute(query)
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name, data):
        try:
            if not data:
                print("Data list is empty. Nothing to insert.")
                return

            placeholders = ', '.join(['?'] * len(data[0]))
            query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            self.conn.executemany(query, data)
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def query_data(self, query):
        try:
            result = pd.read_sql_query(query, self.conn)
            return result
        except sqlite3.Error as e:
            print(f"Error querying data: {e}")
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("SQLite connection closed.")


# Example usage:
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_file = os.path.join(BASE_DIR, 'db', 'my_database.db')

    manager = SQLiteManager(db_file)

    table_name = "videos"
    schema = "video_id TEXT, title TEXT, description TEXT, published_at TEXT, view_count INTEGER, like_count INTEGER, comment_count INTEGER"
    manager.create_table(table_name, schema)

    data = [
    ]
    manager.insert_data(table_name, data)

    query = f"SELECT * FROM {table_name};"
    result = manager.query_data(query)
    print(result)

    manager.close_connection()
