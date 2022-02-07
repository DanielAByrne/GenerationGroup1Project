import pandas as pd
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
    order_prods_df = pd.DataFrame(columns=['orderid', 'prodid', 'quantity', 'price'])

    order_ids_prods = []
    order_prods_ids = []
    order_prods_quantity = []
    order_prods_prices = []

    for i in range(len(orders_df['orderid'])):
        
        i_id = orders_df['orderid'].loc[i]
        order_prods = orders_df['Order'].loc[i].split(',')
        
        for order_prod in order_prods: #split price
            
            if order_prod.count('-') == 1:
                order_prod = order_prod.split('-')
            else:
                order_prod = split(order_prod, '-', 2)

            prod = order_prod[0]
            price = float(order_prod[1])
            
            prod_id = get_prod_id_sql('products',prod,'prodid','prodname',price,'currentprice')
            
            order_ids_prods.append(i_id)
            order_prods_ids.append(prod_id)
            order_prods_quantity.append(1)
            order_prods_prices.append(price)

    order_prods_df['orderid'] = order_ids_prods
    order_prods_df['prodid'] = order_prods_ids
    order_prods_df['quantity'] = order_prods_quantity
    order_prods_df['price'] = order_prods_prices

    order_prods_df.set_index('orderid', inplace=True)
    
    return order_prods_df

def get_prod_id_sql(table_name, product, id_name,var_name,price,price_name):
    
    prod_id_dict = execute_query(f"SELECT {id_name} FROM {table_name} WHERE {var_name} = '{product}'")

    if prod_id_dict == []: # if prod is not in database, query returns empty tuple
        execute_query(f"INSERT INTO {table_name} ({var_name}, {price_name}) VALUES ('{product}', {price})")
        prod_id_dict = execute_query(f"SELECT {id_name} FROM {table_name} WHERE {var_name} = '{product}'")
    
    prod_id = prod_id_dict[0][0]
    return prod_id

def get_id_sql(table_name, branch, id_name, var_name):

    statement = f"SELECT {id_name} FROM {table_name} WHERE {var_name} = '{branch}'"
    branch_id_dict = execute_query(statement)
    
    if branch_id_dict == []: # branch doesn't exist yet
        execute_query(f"INSERT INTO {table_name} ({var_name}) VALUES ('{branch}')")
        branch_id_dict = execute_query(f"SELECT {id_name} FROM {table_name} WHERE {var_name} = '{branch}'")

    branch_id = branch_id_dict[0][0]
    return branch_id

def split(strng, sep, pos):
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])