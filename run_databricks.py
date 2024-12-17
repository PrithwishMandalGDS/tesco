from databricks import sql
import os
import sys

server_hostname = sys.argv[1]
access_token = sys.argv[2]

connection = sql.connect(
    server_hostname=server_hostname,
    http_path="/sql/1.0/warehouses/60751e1cc45a0166",
    access_token=access_token
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