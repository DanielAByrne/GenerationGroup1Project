import os
from dotenv import load_dotenv
import psycopg2
import traceback

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
port = os.environ.get('port')
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

def pandas_to_sql(df,table_name, col_name, mode):

    # Fill in the blanks for the conn object
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()

    # Adjust ... according to number of columns
    try:
        
        np_data = df.to_numpy()
        a = ','.join(["%s"]*len(df.columns))
        col_names = ','.join(df.columns.tolist())
        args_str = b','.join(cursor.mogrify(f"({a})", x) for x in tuple(map(tuple,np_data)))
        
        if mode == 'add':
            cursor.execute(f"insert into {table_name} ({col_names}) VALUES "+args_str.decode("utf-8"))
            
        elif mode == 'join':
            cursor.execute(f"CREATE TEMP TABLE {table_name}_temp AS SELECT * FROM {table_name} LIMIT 0")
            cursor.execute(f"INSERT INTO {table_name}_temp ({col_names}) VALUES "+args_str.decode("utf-8"))
            cursor.execute(f"INSERT INTO {table_name} SELECT * FROM {table_name}_temp WHERE {col_name} NOT IN (SELECT {col_name} FROM {table_name})")
    
    except Exception:
        print(traceback.format_exc())
        
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
        cursor.close()
        connection.close()
