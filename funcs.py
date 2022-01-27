import pandas as pd

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

def get_id(df, branch, id_name):
    try:
        branch_id = df.loc[branch][id_name]
    except:
        if len(df[id_name]) > 0:
            branch_id = df.iloc[-1,0] + 1
        else:
            branch_id = 1
        
        df.loc[branch] = [branch_id]
    
    return branch_id
    
def split(strng, sep, pos):
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])