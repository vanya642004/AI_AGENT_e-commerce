# db_init.py  (run this once manually)
import sqlite3, pandas as pd, glob, os

DB_PATH = "ecommerce.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
for csv in glob.glob("data/*.csv"):
    df = pd.read_csv(csv)
    table = os.path.splitext(os.path.basename(csv))[0].lower()
    df.to_sql(table, conn, if_exists="replace", index=False)
conn.close()
print("Database created!")
