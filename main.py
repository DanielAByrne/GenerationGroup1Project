#%%
import pandas as pd
import numpy as np
from funcs import *
from db import *

#%%
# IMPORT DATA AND CREATE ORDER ID
filepath = 'chesterfield.csv'

orders_df = pd.read_csv(filepath, header=None)
orders_df.columns = ['time_stamp', 'location', 'Customer Name', 'Order', 'sum_total', 'Payment Method', 'Card Number']

#%%
first_id = get_first_order_id('transactions', 'orderid')
order_ids = np.linspace(first_id,first_id + len(orders_df['time_stamp']) - 1, len(orders_df['time_stamp']))
order_ids = order_ids.tolist()
order_ids = [int(i) for i in order_ids]

orders_df['orderid'] = order_ids
orders_df.set_index('orderid', inplace=True)

#%%
# DROP SENSITIVE INFO
orders_df.drop(['Customer Name', 'Card Number'], axis=1, inplace=True)

#%%
# CREATE AND POPULATE BRANCH ID COLUMN

branches = orders_df['location'].tolist()
order_branch_ids = []

for branch in branches:
    order_branch_ids.append(get_id_sql('locations', branch, 'branchid', 'branchname'))

# REPLACE BRANCH NAME WITH BRANCH ID IN ORDERS DATAFRAME
orders_df['branchid'] = order_branch_ids
orders_df.drop(['location'], axis=1, inplace=True)

#%%
# CREATE AND POPULATE PAYMENT METHODS COLUMN

payments = orders_df['Payment Method'].tolist()
order_payment_ids = []

for payment in payments:
    order_payment_ids.append(get_id_sql('payment_method', payment, 'paymentid', 'paymentmethod'))

# REPLACE PAYMENT NAME WITH PAYMENT ID IN ORDERS DATAFRAME
orders_df['paymentid'] = order_payment_ids
orders_df.drop(['Payment Method'], axis=1, inplace=True)

#%%
# CREATE AND POPULATE ORDER PRODUCTS DATAFRAME, UPDATE PRODUCTS TABLE

order_prods_df = pd.DataFrame(columns=['orderid', 'prodid', 'quantity', 'price'])

order_ids_prods = []
order_prods_ids = []
order_prods_quantity = []
order_prods_prices = []

for i in order_ids:
    
    order_prods = orders_df['Order'].iloc[i-first_id].split(',')
    
    for order_prod in order_prods: #split price
        
        if order_prod.count('-') == 1:
            order_prod = order_prod.split('-')
        else:
            order_prod = split(order_prod, '-', 2)

        prod = order_prod[0]
        price = float(order_prod[1])
        
        prod_id = get_prod_id_sql('products',prod,'prodid','prodname',price,'currentprice')
        
        order_ids_prods.append(i)
        order_prods_ids.append(prod_id)
        order_prods_quantity.append(1)
        order_prods_prices.append(price)

order_prods_df['orderid'] = order_ids_prods
order_prods_df['prodid'] = order_prods_ids
order_prods_df['quantity'] = order_prods_quantity
order_prods_df['price'] = order_prods_prices

order_prods_df.set_index('orderid', inplace=True)

orders_df.drop(['Order'], axis=1, inplace=True)

# %%
# REORGANISE COLUMNS
orders_df.reset_index(inplace=True)
orders_df = orders_df[['orderid', 'time_stamp', 'branchid', 'paymentid', 'sum_total']]
orders_df.set_index('orderid', inplace=True)

#%%
# ADD TO DATABASE
alchemy_query(orders_df, 'transactions')

#%%
alchemy_query(order_prods_df, 'order_products')

# %%
