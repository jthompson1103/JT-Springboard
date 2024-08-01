# Step 1: Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 2: Loading the data
url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"
properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col=None)

# Step 3: Exploring the data
print(properties.shape)
print(properties.head())

# Step 4: Cleaning the data (Part 1)
properties_T = properties.T
print(properties_T.head())

properties_T = properties_T.reset_index()
print(properties_T.head())

print(properties_T.index)
print(properties_T.head())

properties_T.columns = properties_T.iloc[0]
properties_T = properties_T.drop(0)
print(properties_T.head())

properties_T = properties_T.rename(columns={'Unnamed: 0': 'London_Borough', pd.NaT: 'ID'})
print(properties_T.head())
print(properties_T.columns)

# Step 5: Transforming the data
clean_properties = pd.melt(properties_T, id_vars=['London_Borough', 'ID'])
clean_properties = clean_properties.rename(columns={0: 'Month', 'value': 'Average_price'})
print(clean_properties.head())

print(clean_properties.dtypes)
clean_properties['Average_price'] = pd.to_numeric(clean_properties['Average_price'])
print(clean_properties.dtypes)
print(clean_properties.count())

# Step 6: Cleaning the data (Part 3)
print(clean_properties['London_Borough'].unique())

nonBoroughs = ['Inner London', 'Outer London', 'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER',
               'EAST MIDLANDS', 'WEST MIDLANDS', 'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST',
               'SOUTH WEST', 'England']

clean_properties = clean_properties[~clean_properties.London_Borough.isin(nonBoroughs)]
df = clean_properties.dropna()
print(df.shape)

# Step 7: Visualizing the data
camden_prices = df[df['London_Borough'] == 'Camden']
ax = camden_prices.plot(kind='line', x='Month', y='Average_price')
ax.set_ylabel('Price')

# Step 8: Further cleaning and transformation
df['Year'] = df['Month'].apply(lambda t: t.year)
print(df.tail())

dfg = df.groupby(by=['London_Borough', 'Year']).mean()
dfg = dfg.reset_index()
print(dfg.head())

# Step 9: Modelling
def create_price_ratio(d):
    y1998 = float(d['Average_price'][d['Year']==1998])
    y2018 = float(d['Average_price'][d['Year']==2018])
    ratio = [y2018 / y1998]
    return ratio

final = {}
for b in dfg['London_Borough'].unique():
    borough = dfg[dfg['London_Borough'] == b]
    final[b] = create_price_ratio(borough)

df_ratios = pd.DataFrame(final).T.reset_index()
df_ratios = df_ratios.rename(columns={'index': 'London_Borough', 0: '2018'})
top15 = df_ratios.sort_values(by='2018', ascending=False).head(15)

ax = top15[['London_Borough', '2018']].plot(kind='bar')
ax.set_xticklabels(top15['London_Borough'])

# Conclusion
print("The boroughs with the greatest increase in housing prices from 1998 to 2018 are:")
print(top15)
