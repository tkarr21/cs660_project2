# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# %%
items = os.listdir('./geo_df/')
p_files = []
for item in items:
    if item == 'iplists' or item == 'whois_responses':
        continue
    p_files += [item]

items = p_files[1:]
items
# %%
df = pd.read_pickle('./geo_df/queries.log-20210829.pkl')

for item in items:
    df1 = pd.read_pickle(f'./geo_df/{item}')
    df = pd.concat([df, df1], axis=0)
    print(item)

# %%
df['dnssec_ok'] = np.where(df['flags'].str.contains('D'), True, False)

# %%
ipv6_df = df[df['server_ip'].str.contains(':')]

# %%
df.to_pickle('2021-08-27-to-31-global.pkl')


# %%
df = pd.read_pickle('2021-08-27-to-31-all.pkl')

# %%

# group by country and qtype and count qtypes
df_fcountry = df.groupby(['country', 'qtype'])[
    'country'].count().unstack('qtype').fillna(0)
