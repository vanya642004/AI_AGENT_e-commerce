import os, sqlite3, pandas as pd

def ensure_database(csv_paths, db_path="ecommerce.db"):
    # create folder if needed
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(db_path)
    for csv in csv_paths:
        if not os.path.exists(csv):
            raise FileNotFoundError(f"{csv} not found")
        df = pd.read_csv(csv)
        name = os.path.splitext(os.path.basename(csv))[0].lower()
        df.to_sql(name, conn, if_exists="replace", index=False)
    conn.close()
