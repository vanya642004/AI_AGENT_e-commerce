import sqlite3
import pandas as pd

def load_data():
    conn = sqlite3.connect("ecommerce.db")
    base = "./data"

    pd.read_csv(f"{base}/total_sales.csv").to_sql("total_sales", conn, if_exists="replace", index=False)
    pd.read_csv(f"{base}/ad_sales.csv").to_sql("ad_sales", conn, if_exists="replace", index=False)
    pd.read_csv(f"{base}/eligibility.csv").to_sql("eligibility", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_data()