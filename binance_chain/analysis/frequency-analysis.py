
import json
# from pandas.io.json import json_normalize
# import pandas as pd
file = 'data.json'
with open(file) as train_file:
    dict_train = json.load(train_file)

print(type(dict_train['timestamp']))
# print(dict_train)
# df = pd.DataFrame.from_dict(json_normalize(dict_train))
#
#
# print(df)
