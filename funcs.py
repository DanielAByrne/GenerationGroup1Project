import pandas as pd
from db import execute_query

def get_first_order_id(table_name, id_name):
    first_id_dict = execute_query(f'SELECT {id_name} FROM {table_name} ORDER BY {id_name} DESC LIMIT 1')
    
    if first_id_dict == ():
        first_id = 1
    else:
        first_id = int(first_id_dict[0][id_name]) + 1
    
    return first_id

def get_prod_id(df, product):
    
    prod_name = product[0]
    price = product[1]
    
    try:
        prod_id = df.loc[prod_name]['Product ID']
        df.loc[prod_name, 'Current Price'] = price
        
    except:
        if len(df['Product ID']) > 0:
            prod_id = df.iloc[-1,0] + 1
        else:
            prod_id = 1
            
        df.loc[prod_name] = [prod_id, price]
        
    return prod_id

def get_prod_id_sql(table_name, product, id_name,var_name,price,price_name):
    
    prod_id_dict = execute_query(f'SELECT {id_name} FROM {table_name} WHERE {var_name} = "{product}"')
    
    if prod_id_dict == ():
        execute_query(f'INSERT INTO {table_name} ({var_name}, {price_name}) VALUES ("{product}", {price})')
        prod_id_dict = execute_query(f'SELECT {id_name} FROM {table_name} WHERE {var_name} = "{product}"')
    
    prod_id = prod_id_dict[0][id_name]
    return prod_id

def get_id_sql(table_name, branch, id_name, var_name):

    branch_id_dict = execute_query(f'SELECT {id_name} FROM {table_name} WHERE {var_name} = "{branch}"')
    
    if branch_id_dict == (): # branch doesn't exist yet
        execute_query(f'INSERT INTO {table_name} ({var_name}) VALUES ("{branch}")')
        branch_id_dict = execute_query(f'SELECT {id_name} FROM {table_name} WHERE {var_name} = "{branch}"')
    
    branch_id = branch_id_dict[0][id_name]
    return branch_id

def split(strng, sep, pos):
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])