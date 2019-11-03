from binance_chain.environment import BinanceChainEnvironment
from binance_chain.http import ExplorerApiClient
from binance_chain.constants import TransactionType
import json
from datetime import datetime
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns


env = BinanceChainEnvironment.get_production_env()

client = ExplorerApiClient(env)

proposal_list = list()

def get_list(txList):
    for i in txList:
        #print(datetime.fromtimestamp(i['timeStamp']/1000).date(),i['blockHeight'])
        proposal_list.append(datetime.fromtimestamp(i['timeStamp']/1000).date())

def add_week_of_month(df):
    df['week_in_month'] = pd.to_numeric(df.index.day/7)
    df['week_in_month'] = df['week_in_month'].apply(lambda x: math.ceil(x))
    return df

## get the total count
res = client.get_transactions(
    tx_type=TransactionType.PROPOSAL,
    page=1,
    rows=1
)

print(type(res))
print(res)
total_tx = res['txNums']

app_json = json.dumps(res)
print(type(app_json))

print(res['txNums'])

## loop to get all timestamples
for i in range(3):
    print(i)
    res = client.get_transactions(
        tx_type=TransactionType.PROPOSAL,
        page=i+1,
        rows=100
    )
    print("len: ",len(res['txArray']))
    get_list(res['txArray'])

dict = {}

print(len(proposal_list))
# hash = json.dumps(proposal_list)
#
# dict['timestamp']= hash
## save to json file
# proposal_data = json.dumps(proposal_list)
# f = open("data.json","w")
# f.write(proposal_data)
# f.close()
#
# history = json.load("data.json","r")
# print(type(history))

df = pd.DataFrame(proposal_list,columns =['Time'])
df['value'] = pd.Series(np.ones(df.shape[0]),index=df.index)

#print(df)

df2 = df.loc[:,['value']]
## 统计出现频率
df2['week_no'] = pd.to_datetime(df['Time']).dt.week
df2['month_no'] = pd.to_datetime(df['Time']).dt.month
df2['day_of_month'] = pd.to_numeric(pd.to_datetime(df['Time']).dt.day)

#print(df2)

## 打印
df3 = (df2.groupby('week_no').sum().reset_index())
#print(df3)

#print(df3['value'].values[0])

## Draw Heatmap

# month_list =  ['January', 'February', 'March', 'April', 'May', 'June', 'July',
#           'August', 'September', 'October', 'November', 'December']
#
# week_list = [1,2,3,4]

pt = df2.pivot_table(index='month_no', columns='day_of_month', values='value', aggfunc=np.sum)
pt.head()
print(pt)


f, ax = plt.subplots(figsize = (35, 9))

#cmap = sns.cubehelix_palette(start = 0, rot = 3, gamma=0.8)
cmap = sns.cubehelix_palette(light=1, as_cmap=True)

figure = sns.heatmap(pt,yticklabels=True, linewidths = 0.01, ax = ax, vmax=10, vmin=0, cmap=cmap,annot= True,square = True)
ax.set_title('Proposal count')
ax.set_xlabel('Month')
ax.set_ylabel('Day of month')
plt.show()
f.savefig('sns_heatmap_normal.png', bbox_inches='tight')
# ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)

# f,ax = plt.subplots(figsize=(10,5))
# pic = sns.heatmap(pt, annot=True, fmt="d", ax=ax)
# f.savefig('sns_heatmap_normal.png', bbox_inches='tight')
