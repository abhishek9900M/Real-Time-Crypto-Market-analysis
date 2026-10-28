import time
from datetime import datetime

import pandas as pd
import requests

from Data_pipeline_insertion2 import insert_crypto_snapshot


API_URL = "https://api.coingecko.com/api/v3/coins/markets"
API_KEY = "CG-2uqniyR42XU9iC2vv3Y6RS5V"
HEADERS = {"x-cg-demo-api-key": API_KEY}
PAGES = (1, 2, 3)
PER_PAGE = 250
REFRESH_SECONDS = 10
EXCEL_PATH = "Coin-geco-market-data.xlsx"

while True:

        all_data = []

        # Fetch every requested page successfully before touching SQL Server.
        # If any page fails, skip this cycle so an incomplete snapshot cannot
        # delete a previous complete snapshot.
        for page in PAGES:
            params = {
                "vs_currency": "usd",
                "order": "current_price_desc",
                "page": page,
                "per_page": PER_PAGE,
                "sparkline": False,}

            response = requests.get(API_URL,params=params,headers=HEADERS,timeout=30,)
            page_data = response.json()

            print(f"Page {page} records: {len(page_data)}")
            all_data.extend(page_data)

        df = pd.DataFrame(all_data)
        required = ["id", "name", "current_price"]
        df = df.drop(columns=["image","ath","ath_change_percentage","ath_date","atl","atl_change_percentage","al_date","roi",],errors="ignore",)

        df["Collected_At"] = datetime.now()
        df = df.dropna(subset=["id", "name", "current_price"])
        df = df.drop_duplicates(subset=["id"], keep="last")
        df  = df.fillna(0)

        # Replace the SQL snapshot only after all API pages were fetched and
        # validated. This function inserts all rows and deletes older rows.
        inserted, deleted = insert_crypto_snapshot(df)
        print(f"SQL snapshot complete: {inserted} inserted; "f"{deleted} previous rows deleted.")

        # Excel export is separate; an Excel file lock should not invalidate SQL.
        df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")
        print("Excel file updated successfully.")
        print("Pls wait 40s for next update...")
        time.sleep(20)
