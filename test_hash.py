import pandas as pd

df=pd.read_csv("chesterfield_25-08-2021_09-00-00.csv")

df.columns=["TimeStamp","BranchID","Order","Total","PayMethod","CardNo"]

df["Order"]=df["Order"].apply(lambda x: x.split(","))

df=df.explode("Order")