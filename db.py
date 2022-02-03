import pymysql
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

def alchemy_query(df,table_name):
    msqldb_uri = f'mysql+pymysql://{user}:{password}@{host}/{database}'
    engine = create_engine(msqldb_uri)
    df.to_sql(table_name, con=engine, if_exists='append')

# Establish a database connection
def execute_query(statement, host=host,user=user,password=password,database=database):
    connection = pymysql.connect(host,user,password,database, autocommit=True)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(statement)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows
