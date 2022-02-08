import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
port = os.environ.get('port')
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

def pandas_to_sql(df,table_name):
    msqldb_uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(msqldb_uri)
    df.to_sql(table_name, con=engine, if_exists='append')

# Establish a database connection
def execute_query(statement):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        cursor.execute(statement)
        connection.commit()
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

