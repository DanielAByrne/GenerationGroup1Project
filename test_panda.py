import pandas as pd

filepath = 'chesterfield.csv'

orders_df = pd.read_csv(filepath)
orders_df.columns = ["Timestamp", "Location", "Customer Name", "Order", "Total Cost", "Payment Method", "Card Number"]

# DROP SENSITIVE INFO
orders_df.drop(["Card Number"], axis=1, inplace=True)

# CREATE AND POPULATE CUSTOMERS DATAFRAME
customers_df = pd.DataFrame(columns = ['Customer ID','Customer Name'])
# populate here

# CREATE AND POPULATE ORDER PRODUCTS DATAFRAME
prods_df = orders_df['Order'].str.split(',')
print(prods_df)