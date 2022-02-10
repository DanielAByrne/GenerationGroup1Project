import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
port = os.environ.get('port')
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

def pandas_to_sql(df,table_name):

    # Fill in the blanks for the conn object
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()

    # Adjust ... according to number of columns
    np_data = df.to_numpy()
    a = ','.join(["%s"]*len(df.columns))
    col_names = ','.join(df.columns.tolist())
    args_str = b','.join(cursor.mogrify(f"({a})", x) for x in tuple(map(tuple,np_data)))
    cursor.execute(f"insert into {table_name} ({col_names}) VALUES "+args_str.decode("utf-8"))

    cursor.close()
    connection.commit()
    connection.close()

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

