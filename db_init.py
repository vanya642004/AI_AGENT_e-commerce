from sqlalchemy import create_engine
import pandas as pd
from typing import Dict


def init_db_from_dfs(dfs: Dict[str, pd.DataFrame]):
    """
    Create an in-memory SQLite database and load each DataFrame as a table.
    Table names are derived from the filename (without .csv).
    """
    engine = create_engine("sqlite:///:memory:")
    for fname, df in dfs.items():
        # derive table name
        table = fname.rsplit('.', 1)[0].replace(' ', '_').lower()
        df.to_sql(table, engine, if_exists='replace', index=False)
    return engine
