import re
# my_list = ["Large Flavoured iced latte - Caramel - 3.25, Regular Flavoured iced latte - Hazelnut - 2.75, Regular Flavoured iced latte - Caramel - 2.75, Large Flavoured iced latte - Hazelnut - 3.25, Regular Flavoured latte - Hazelnut - 2.55, Regular Flavoured iced latte - Hazelnut - 2.75"]

# # # my_list=[i.split('\t')[0] for i in my_list]
# my_list=[i.split(',') for i in my_list]

# print(my_list)

# Below only works for int that are seperate to string
# from collections import defaultdict
# listDict = defaultdict(list)
# for x in my_list:
#     listDict[type(x)].append(x)
# print(listDict[int])
# print(listDict[str])

# # df = df["Order"]
# orders = []
# for order in my_list:
#     orders+=order.split(',')

# print(orders)

inp = "Large Latte - 2.45, Large Flavoured iced latte - Vanilla - 3.25, Large Flavoured iced latte - Hazelnut - 3.25"

# inp="Large Flat white - 2.45, Large Latte - 2.45, Large Flavoured latte - Hazelnut - 2.85, Regular Flavoured latte - Hazelnut - 2.55"
d = dict(re.findall(r'(.*?)\s*-\s*(\d+(?:\.\d+)?),?\s*', inp))
print(d)

# with open("chesterfield_25-08-2021_09-00-00.csv", "r") as f:
#     for row in f