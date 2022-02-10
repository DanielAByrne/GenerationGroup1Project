from funcs import *
from db import *

def main_etl(filepath):
# CREATE ORDERS DATAFRAME
    columns = ['time_stamp', 'location', 'Customer Name', 'Order', 'sum_total', 'Payment Method', 'Card Number']

    orders_df = create_dataframe(filepath,columns)

    # CREATE ORDER IDS AND SET THEM AS THE INDEX OF THE ORDERS DATAFRAME
    orders_df = create_order_ids(orders_df)

    # DROP SENSITIVE INFO
    orders_df.drop(['Customer Name', 'Card Number'], axis=1, inplace=True)

    # CREATE AND POPULATE BRANCH ID COLUMN
    orders_df = create_ids(orders_df, 'location','branchid','branchname', 'locations')

    # CREATE AND POPULATE PAYMENT METHODS COLUMN
    orders_df = create_ids(orders_df, 'Payment Method', 'paymentid', 'paymentmethod','payment_method')

    # CREATE AND POPULATE ORDER PRODUCTS DATAFRAME, UPDATE PRODUCTS TABLE
    order_prods_df = create_order_prods(orders_df)

    # REORGANISE COLUMNS
    orders_df = orders_df[['orderid', 'time_stamp', 'branchid', 'paymentid', 'sum_total']]
    order_prods_df = order_prods_df[['orderid', 'prodid', 'quantity', 'price']]

    # ADD TO DATABASE
    pandas_to_sql(orders_df, 'transactions')
    pandas_to_sql(order_prods_df, 'order_products')

