import os
import sqlite3
import pandas as pd


def ensure_database(csv_paths, db_path="ecommerce.db"):
    """
    Reads each CSV file in csv_paths into a SQLite database at db_path.
    Each CSV becomes a table named after the CSV filename (without extension).
    """
    # If database exists, skip creation
    if os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    for csv_file in csv_paths:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        df = pd.read_csv(csv_file)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        # Normalize table name: lowercase, replace spaces with underscores
        table_name = table_name.strip().lower().replace(" ", "_")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
