import pandas as pd
from SQL_Connect import conn


COLUMNS = [
    "id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "market_cap_rank",
    "fully_diluted_valuation",
    "total_volume",
    "high_24h",
    "low_24h",
    "price_change_24h",
    "price_change_percentage_24h",
    "market_cap_change_24h",
    "market_cap_change_percentage_24h",
    "circulating_supply",
    "total_supply",
    "max_supply",
    "last_updated",
    "Collected_At",
]


def insert_crypto_snapshot(df):
    """Replace older SQL snapshot rows with the latest complete API dataset.

    The DELETE and INSERT happen in one transaction. If insertion fails, rollback
    restores the previous rows. This function performs no UPDATE operations.
    """
    data = df.loc[:, COLUMNS].copy()
    data = data.dropna(subset=["id", "name", "current_price"])
    data = data.drop_duplicates(subset=["id"], keep="last")
  
    if data.empty:
        raise ValueError("No valid coin rows; SQL snapshot was not changed.")

    # SQL Server DATETIME does not accept timezone-aware values. Store last_updated
    # as a timezone-naive UTC datetime.
    data["last_updated"] = (pd.to_datetime(data["last_updated"], errors="coerce", utc=True).dt.tz_localize(None))
    data["Collected_At"] = pd.to_datetime(data["Collected_At"], errors="coerce")

    collection_time = data["Collected_At"].max()
    if pd.isna(collection_time):
        raise ValueError("Collected_At is missing; SQL snapshot was not changed.")

    collection_time = collection_time.to_pydatetime()
    data["Collected_At"] = collection_time

    # Convert pandas/numpy scalars and NaN values to pyodbc-friendly values.
    records = []
    for row in data.itertuples(index=False, name=None):
        values = []
        for value in row:
            if pd.isna(value):
                values.append(None)
            elif isinstance(value, pd.Timestamp):
                values.append(value.to_pydatetime())
            elif hasattr(value, "item"):
                values.append(value.item())
            else:
                values.append(value)
        records.append(tuple(values))

    insert_sql = """
        INSERT INTO dbo.cryptocaol (
            id, symbol, name, current_price, market_cap,
            market_cap_rank, fully_diluted_valuation, total_volume,
            high_24h, low_24h, price_change_24h,
            price_change_percentage_24h, market_cap_change_24h,
            market_cap_change_percentage_24h, circulating_supply,
            total_supply, max_supply, last_updated, Collected_At
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursor = conn.cursor()
    try:
        # Delete rows from earlier collections. Keep delete and insert in the
        # same transaction, so a failed insert can be rolled back safely.
        cursor.execute(
            """
            DELETE FROM dbo.cryptocaol
            WHERE Collected_At < ? OR Collected_At IS NULL
            """,
            (collection_time,),
        )
        deleted_count = cursor.rowcount

        cursor.executemany(insert_sql, records)
        conn.commit()

        print(f"Previous collection rows deleted: {deleted_count}")
        print(f"Current collection rows inserted: {len(records)}")
        print(f"Collected_At: {collection_time}")
        return len(records), deleted_count

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
