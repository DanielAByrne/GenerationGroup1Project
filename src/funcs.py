import pandas as pd
import numpy as np
from db import execute_query

def create_dataframe(filepath,columns):
    df = pd.read_csv(filepath, header=None)
    df.columns = columns
    return df

def create_order_ids(df):
    order_ids = df.apply(lambda x: abs(hash(x["time_stamp"] + x["Customer Name"])), axis=1)
    df['orderid'] = order_ids
    
    return df

def create_ids(df,col_name_df,id_name,col_name_sql,table_name_sql):
    col = df[col_name_df].tolist()
    col_ids = []

    for elem in col:
        col_ids.append(get_id_sql(table_name_sql, elem, id_name, col_name_sql))

    df[id_name] = col_ids
    df.drop([col_name_df], axis=1, inplace=True)
    
    return df

def create_order_prods(orders_df):
    
    order_prods_df = orders_df[['orderid', 'Order']]
    order_prods_df['Order'] = order_prods_df['Order'].apply(lambda x: x.split(', '))

    order_prods_df = order_prods_df.explode('Order')
    order_prods_df['quantity'] = np.ones(len(order_prods_df['orderid'])).tolist()

    order_prods_df = order_prods_df.groupby(['orderid', 'Order']).count()['quantity'].reset_index()
    dummy_df = order_prods_df['Order'].str.rpartition(' - ') # split column in last occurrence of separator

    order_prods_df['Order'] = dummy_df[0]
    order_prods_df['price'] = dummy_df[2]

    order_prods_ids = []
    count = 0
        
    for order_prod in order_prods_df['Order'].tolist(): 
        
        price = float(order_prods_df.loc[count,'price'])

        prod_id = get_prod_id_sql('products',order_prod,'prodid','prodname',price,'currentprice')
        
        order_prods_ids.append(prod_id)
        count += 1

    order_prods_df.drop(['Order'], axis=1, inplace=True)
    order_prods_df['prodid'] = order_prods_ids
    
    return order_prods_df

def get_prod_id_sql(table_name, product, id_name,var_name,price,price_name):
    
    prod_id_dict = execute_query(f"SELECT {id_name} FROM team1_schema.{table_name} WHERE {var_name} = '{product}'")

    if prod_id_dict == []: # if prod is not in database, query returns empty tuple
        execute_query(f"INSERT INTO team1_schema.{table_name} ({var_name}, {price_name}) VALUES ('{product}', {price})")
        prod_id_dict = execute_query(f"SELECT {id_name} FROM team1_schema.{table_name} WHERE {var_name} = '{product}'")
    
    prod_id = prod_id_dict[0][0]
    return prod_id

def get_id_sql(table_name, branch, id_name, var_name):

    statement = f"SELECT {id_name} FROM team1_schema.{table_name} WHERE {var_name} = '{branch}'"
    branch_id_dict = execute_query(statement)
    if branch_id_dict == []: # branch doesn't exist yet
        execute_query(f"INSERT INTO team1_schema.{table_name} ({var_name}) VALUES ('{branch}')")
        branch_id_dict = execute_query(f"SELECT {id_name} FROM team1_schema.{table_name} WHERE {var_name} = '{branch}'")

    branch_id = branch_id_dict[0][0]
    return branch_id

#test