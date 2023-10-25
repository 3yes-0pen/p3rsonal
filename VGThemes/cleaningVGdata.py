import pandas as pd
import re
from html import unescape

VGsales = pd.read_csv('~/Python/VGThemes/updatedVGSales.csv')
VGoutput = pd.read_csv('~/Python/VGThemes/updatedVGOutput.csv')

VGoutput = VGoutput.rename(columns={'name': 'Name', 'platform': 'Platform', 'release_date': 'Year'})
VGsales['user_rating'] = None
VGsales = VGsales.astype({
    'Name': str,
    'Platform': 'category',
    'Year': float,
    'Publisher': 'category',
    'description': object,
    'metacritic': float
})
VGoutput['Year'] = pd.to_datetime(VGoutput['Year'])
# Extract year and convert to float
VGoutput['Year'] = VGoutput['Year'].dt.year.astype(float)
VGoutput['Publisher'] = None
VGoutput = VGoutput.astype({
    'Name': str,
    'Platform': 'category',
    'user_rating': 'float64',
    'critic_rating': 'int64',
    'Year': float,
    'summary': object,
    'description': object,
    'metacritic': float
})
columns_included = ['Name', 'Platform', 'Publisher', "Year", "metacritic", "user_rating"]
VGoutput_select = VGoutput[columns_included]
VGsales_select = VGsales[columns_included]
VGdata = pd.concat([VGoutput_select, VGsales_select], ignore_index=False)

VGdata['Year'] = VGdata['Year'].astype(pd.Int64Dtype())
VGdata['metacritic'] = VGdata['metacritic'].astype(pd.Int64Dtype())
VGdata = VGdata.sort_values(by='Year', ascending=True)
print(VGdata.head(15))
VGdata = VGdata.dropna(subset=['Year'])
VGdata.to_csv('~/Python/input/VGdataaa.csv', index=False)