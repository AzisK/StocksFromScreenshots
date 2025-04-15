from datetime import datetime

import duckdb

from constants import DB_PATH

TABLE_NAME = "trades"


def execute_query(query):
    with duckdb.connect(DB_PATH) as conn:
        print("Executing: ", query)
        conn.execute(query)


def fetch_df(query):
    with duckdb.connect(DB_PATH) as conn:
        return conn.execute(query).fetchdf()


def save_to_database(df):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_name_with_timestamp = f"{TABLE_NAME}_{timestamp}"

    with duckdb.connect(DB_PATH) as conn:
        conn.register(table_name_with_timestamp, df)
        columns = ", ".join(df.columns)
        insert_query = f"INSERT INTO {TABLE_NAME} ({columns}) SELECT {columns} FROM {table_name_with_timestamp}"
        print("Executing:\n", insert_query)
        conn.execute(insert_query)


def overwrite_database(df):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_name_with_timestamp = f"{TABLE_NAME}_{timestamp}"

    with duckdb.connect(DB_PATH) as conn:
        conn.register(table_name_with_timestamp, df)
        delete_query = f"DELETE FROM {TABLE_NAME}"
        print("Executing:\n", delete_query)
        conn.execute(delete_query)
        columns = ", ".join(df.columns)
        insert_query = f"INSERT INTO {TABLE_NAME} ({columns}) SELECT {columns} FROM {table_name_with_timestamp}"
        print("Executing:\n", insert_query)
        conn.execute(insert_query)


def load_existing_trades():
    return fetch_df(f"SELECT * FROM {TABLE_NAME}")


def update_file_name_in_db(old_file_name, new_file_name):
    execute_query("UPDATE ? SET file = ? WHERE file = ?", (TABLE_NAME, new_file_name, old_file_name))
