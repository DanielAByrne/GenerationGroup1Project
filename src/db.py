import os
import psycopg2
import traceback
from json import loads
import boto3


client2 = boto3.client('ssm')
response = client2.get_parameter(Name='team1_creds',WithDecryption=True)
creds = loads(response['Parameter']['Value'])

host = creds["host"]
user = creds["user"]
port = creds["port"]
password = creds["password"]
database = "team1_cafe"


def pandas_to_sql(df,table_name, col_name, mode):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        np_data = df.to_numpy()
        a = ','.join(["%s"]*len(df.columns))
        col_names = ','.join(df.columns.tolist())
        args_str = b','.join(cursor.mogrify(f"({a})", x) for x in tuple(map(tuple,np_data)))
        
        if mode == 'add':
            cursor.execute(f"insert into team1_schema.{table_name} ({col_names}) VALUES "+args_str.decode("utf-8"))
            
        elif mode == 'join':
            cursor.execute(f"CREATE TEMP TABLE team1_schema.{table_name}_temp AS SELECT * FROM {table_name} LIMIT 0")
            cursor.execute(f"INSERT INTO team1_schema.{table_name}_temp ({col_names}) VALUES "+args_str.decode("utf-8"))
            cursor.execute(f"INSERT INTO team1_schema.{table_name} SELECT * FROM team1_schema.{table_name}_temp WHERE {col_name} NOT IN (SELECT {col_name} FROM team1_schema.{table_name})")
    
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