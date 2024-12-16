from databricks import sql
import os

connection = sql.connect(
    server_hostname="dbc-79d364f2-dcf6.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/60751e1cc45a0166",
    access_token="dapid405b05d0e434e0f5ef52bb3b73f9310"
)

cursor = connection.cursor()

sql_file_path = "output.sql"
try:
    with open(sql_file_path, "r") as file:
        sql_query = file.read()
    cursor.execute(sql_query)
    
    print(cursor.fetchall())

finally:
    cursor.close()
    connection.close()