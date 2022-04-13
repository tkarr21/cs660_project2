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
df.to_pickle('2021-08-27-to-31-global.pkl')


# %%
df = pd.read_pickle('2021-08-27-to-31-global.pkl')


# %%
len(df.index)
# %%
df['dnssec_ok'] = np.where(df['flags'].str.contains('D'), True, False)

# %%
df['ip_prot'] = np.where(df['server_ip'].str.contains(':'), 'ipv6', 'ipv4')
# %%
# ALL QUERIES
df.groupby('dnssec_ok').sum().plot(
    title='DNSSEC OK: All Queries', kind='pie', autopct='%1.0f%%', subplots=True, ylabel='')

# %%
df.head(5)

# %%
# GROUP BY COUNTRY/QTYPE (switch 'country' and 'qtype')
country_df = mic_df.groupby(['qtype', 'dnssec_ok'])[
    'qtype'].count().unstack('dnssec_ok').fillna(0)
# %%
# get top requesting countries
country_df['total'] = country_df[False] + country_df[True]
top_countries = country_df.nlargest(20, 'total').index.tolist()
country_df = country_df.drop(['total'], axis=1)
top_countries_df = country_df.loc[country_df.index.isin(top_countries)]

# %%
df.loc[]
# %%
top_countries_df.head(21)
# %%
# sum remaining countries into one row
remaining_df = country_df[country_df.index.isin(top_countries) == False]

top_countries_df.loc['Combined'] = [
    remaining_df[False].sum(), remaining_df[True].sum()]

# %%
# plot
top_countries_df.plot(kind='bar', logy=True,
                      title='DNSSEC OK: top requesting ASNs', ylabel='num requests', figsize=(10, 6))
plt.legend(loc='lower right')
plt.show()
# %%
dnssec_rrtypes = ['DNSKEY', 'RRSIG', 'CDNSKEY',
                  'NSEC', 'NSEC3', 'NSEC3PARAM', 'DS', 'CDS', 'TA', 'DLV']

# %%
top_countries_df['TpF'] = top_countries_df[True] / top_countries_df[False]
# %%
top_countries_df.head(21)
# %%
dnssec_df = country_df.loc[dnssec_rrtypes]
dnssec_df['TpF'] = dnssec_df[True] / dnssec_df[False]
dnssec_df.head(10)
# %%
df.loc[df['qtype'].isin(
    ['NSEC', 'CDNSKEY', 'NSEC3', 'NSEC3PARAM', 'CDS', 'TA', 'DLV'])]
# %%
# IPv4 vs. IPv6
ip_df = df.groupby(['ip_prot', 'dnssec_ok'])[
    'ip_prot'].count().unstack('dnssec_ok').fillna(0)

ip_df.plot(kind='bar', logy=True,
           title='DNSSEC OK: IP protocols', ylabel='num requests')

# %%
ip_df['TpF'] = ip_df[True] / ip_df[False]
ip_df.head(5)
# %%
ipv6_df = df.loc[df['ip_prot'] == 'ipv6']
# %%
len(ipv6_df.loc[ipv6_df['location'] != 'BYU, US'].index)
# %%
cname_df = df.loc[df['qtype'] == 'CNAME']

# %%
cname_df.loc[cname_df['dnssec_ok'] == False].head(100)
# %%
in_df = df.loc[df['country'] == 'IN']
# %%
in_df.loc[in_df['dnssec_ok'] == False]
# %%
in_df.loc[in_df['qtype'] == 'CNAME']
# %%
mic_df = df.loc[df['location'] == 'MICROSOFT-CORP-MSN-AS-BLOCK, US']
mic_df.head(5)
# %%
