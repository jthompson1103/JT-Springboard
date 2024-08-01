#Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#assigning url to the data frame, and Printing first few rows
url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"
properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col=None)
print(properties.head())

#Cleaning transforming and visualizing
print(properties.info())
print(properties.describe())
print(properties.columns)
print(properties.head())

#Transposing and cleaning the data
properties = properties.transpose()

# Reset the index
properties.reset_index(inplace=True)

# Assign the first row to the header
properties.columns = properties.iloc[0]
properties = properties[1:]

# Rename the first column to 'Month'
properties.rename(columns={'Unnamed: 0': 'Month'}, inplace=True)

# Check the DataFrame after these operations
print(properties.head())
print(properties.columns)

#Melting the data frame
properties_melted = properties.melt(id_vars=['Month'], var_name='London_Borough', value_name='Average_Price')
print(properties_melted.head())
# Inspect the unique values in the 'Month' column
print(properties_melted['Month'].unique())

# Filter out any non-date values from the 'Month' column
valid_months = properties_melted['Month'].str.contains(r'^\d{4}-\d{2}-\d{2}$', na=False)
properties_melted = properties_melted[valid_months]

# Convert 'Average_Price' to float and drop NaN values
properties_melted['Average_Price'] = pd.to_numeric(properties_melted['Average_Price'], errors='coerce')
properties_melted.dropna(subset=['Average_Price'], inplace=True)

# Convert 'Month' to datetime
properties_melted['Month'] = pd.to_datetime(properties_melted['Month'], format='%Y-%m-%d', errors='coerce')

# Drop rows where 'Month' conversion failed
properties_melted.dropna(subset=['Month'], inplace=True)

# Extract year from 'Month'
properties_melted['Year'] = properties_melted['Month'].dt.year

print(properties_melted.head())

#Visualizing the data
# Example: Visualize the housing prices for a specific borough
borough = 'Camden'
borough_data = properties_melted[properties_melted['London_Borough'] == borough]
plt.figure(figsize=(10, 5))
plt.plot(borough_data['Year'], borough_data['Average_Price'])
plt.title(f'Average Housing Prices in {borough}')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.show()

def create_price_ratio(df, borough):
    price_1998 = df[(df['London_Borough'] == borough) & (df['Year'] == 1998)]['Average_Price'].mean()
    price_2018 = df[(df['London_Borough'] == borough) & (df['Year'] == 2018)]['Average_Price'].mean()
    ratio = price_2018 / price_1998
    return ratio

boroughs = properties_melted['London_Borough'].unique()
ratios = {borough: create_price_ratio(properties_melted, borough) for borough in boroughs}

# Display the boroughs with the greatest increase in housing prices
ratios_series = pd.Series(ratios)
ratios_series.sort_values(ascending=False, inplace=True)
print(ratios_series.head(10))

# Conclusion
print("The boroughs with the greatest increase in housing prices from 1998 to 2018 are:")
print(ratios_series.head(10))
