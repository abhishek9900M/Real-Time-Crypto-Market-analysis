import pyodbc


conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=AVEE\SQLEXPRESS;"
    r"DATABASE=realtimecryptodata;"
    r"Trusted_Connection=yes;"
    r"TrustServerCertificate=yes;"
)

print("SQL Server connected successfully!")


