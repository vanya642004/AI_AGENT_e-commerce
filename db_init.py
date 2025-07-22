import os
import pandas as pd
from sqlalchemy import create_engine


def init_db(db_path: str = "ecom.db", data_dir: str = "data"):
    # Create SQLite engine and load CSVs into tables
    engine = create_engine(f"sqlite:///{db_path}")
    tables = {
        "total_sales.csv": "total_sales",
        "ad_sales.csv": "ad_sales",
        "eligibility.csv": "eligibility",
    }
    for fname, table in tables.items():
        path = os.path.join(data_dir, fname)
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="replace", index=False)
    return engine
