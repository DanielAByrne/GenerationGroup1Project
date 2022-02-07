import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from db import *

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
port = os.environ.get('port')
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

statement = f"SELECT branchid FROM locations WHERE Branchname = 'Chesterfield'"
execute_query(statement)

# try:
#     connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
#     cursor = connection.cursor()

#     #statement = "INSERT INTO products (prodname, currentprice) VALUES ('Water', 2.50)"
#     statement = f"SELECT branchid FROM locations WHERE Branchname = 'Chesterfield'"
#     cursor.execute(statement)

#     connection.commit()
#     count = cursor.rowcount
#     rows = cursor.fetchall()
#     print(rows)
#     print(count, "Record inserted successfully into mobile table")

# except (Exception, psycopg2.Error) as error:
#     print("Failed to insert record into mobile table", error)

# finally:
#     # closing database connection.
#     if connection:
#         cursor.close()
#         connection.close()