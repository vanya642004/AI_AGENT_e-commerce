import os
import sqlite3
import pandas as pd

def ensure_database(csv_paths, db_path="ecommerce.db"):
    """
    Reads each CSV in `csv_paths` into a SQLite database at `db_path`.
    Overwrites tables if they already exist.
    """
    # Recreate DB to pick up any CSV changes
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    for csv_file in csv_paths:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        df = pd.read_csv(csv_file)
        table = os.path.splitext(os.path.basename(csv_file))[0] \
                    .strip().lower().replace(" ", "_")
        df.to_sql(table, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
