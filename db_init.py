import os
import sqlite3
import pandas as pd

def ensure_database(csv_paths, db_path="ecommerce.db"):
    """
    Read each CSV in `csv_paths` into SQLite at `db_path`.
    Overwrite any existing DB so you pick up changes.
    """
    # 1) remove old DB
    if os.path.exists(db_path):
        os.remove(db_path)

    # 2) write each CSV as its own table
    conn = sqlite3.connect(db_path)
    for csv_file in csv_paths:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        df = pd.read_csv(csv_file)
        table = (
            os.path.splitext(os.path.basename(csv_file))[0]
            .strip()
            .lower()
            .replace(" ", "_")
        )
        df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()
