import pyodbc as odbc

def get_connection():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=CRISTIAN_PICO\\SQLEXPRESS;"
        "DATABASE=ScuolaDb;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return odbc.connect(connection_string)

def get_database():
    conn = get_connection()

    try:
        yield conn
    finally:
        conn.close()