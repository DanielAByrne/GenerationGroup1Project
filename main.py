#%%
import pandas as pd
import numpy as np
from funcs import *

#%%
# IMPORT DATA AND CREATE ORDER ID
filepath = 'chesterfield.csv'

orders_df = pd.read_csv(filepath)
orders_df.columns = ["Timestamp", "Location", "Customer Name", "Order", "Total Cost", "Payment Method", "Card Number"]

first_id = get_first_order_id('transactions', 'OrderID')
order_ids = np.linspace(first_id,first_id + len(orders_df['Timestamp']), len(orders_df['Timestamp']))
order_ids = order_ids.tolist()
order_ids = [int(i) for i in order_ids]

orders_df['Order ID'] = order_ids
orders_df.set_index('Order ID', inplace=True)


#%%
# DROP SENSITIVE INFO
orders_df.drop(['Customer Name', 'Card Number'], axis=1, inplace=True)

#%%
# CREATE AND POPULATE BRANCH ID COLUMN

branches = orders_df['Location'].tolist()
order_branch_ids = []

for branch in branches:
    order_branch_ids.append(get_id_sql('locations', branch, 'BranchID', 'BranchName'))

# REPLACE BRANCH NAME WITH BRANCH ID IN ORDERS DATAFRAME
orders_df['Branch ID'] = order_branch_ids
orders_df.drop(['Location'], axis=1, inplace=True)

#%%
# CREATE AND POPULATE PAYMENT METHODS COLUMN

payments = orders_df['Payment Method'].tolist()
order_payment_ids = []

for payment in payments:
    order_payment_ids.append(get_id_sql('payment_method', payment, 'PaymentID', 'PaymentMethod'))

# REPLACE PAYMENT NAME WITH PAYMENT ID IN ORDERS DATAFRAME
orders_df['Payment ID'] = order_payment_ids
orders_df.drop(['Payment Method'], axis=1, inplace=True)

#%%
# CREATE AND POPULATE ORDER PRODUCTS DATAFRAME, UPDATE PRODUCTS TABLE

order_prods_df = pd.DataFrame(columns=['Order ID', 'Product ID', 'Quantity', 'Price Paid'])

order_ids_prods = []
order_prods_ids = []
order_prods_quantity = []
order_prods_prices = []

for i in order_ids:
    
    print(i-first_id-1)
    order_prods = orders_df['Order'].iloc[i-first_id-1].split(',')
    
    for order_prod in order_prods:
        
        if order_prod.count('-') == 1:
            order_prod = order_prod.split('-')
        else:
            order_prod = split(order_prod, '-', 2)

        prod = order_prod[0]
        price = float(order_prod[1])
        
        prod_id = get_prod_id_sql('products',prod,'ProdID','ProdName',price,'CurrentPrice')
        
        order_ids_prods.append(i)
        order_prods_ids.append(prod_id)
        order_prods_quantity.append(1)
        order_prods_prices.append(price)

order_prods_df['Order ID'] = order_ids_prods
order_prods_df['Product ID'] = order_prods_ids
order_prods_df['Quantity'] = order_prods_quantity
order_prods_df['Price Paid'] = order_prods_prices

order_prods_df.set_index('Order ID', inplace=True)

orders_df.drop(['Order'], axis=1, inplace=True)
# %%
