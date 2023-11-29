import pandas as pd
import requests

geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
geojson_data = requests.get(geojson_url).json()
# "NAME" field from GeoJSON extracted -> a DataFrame
geo_df = pd.DataFrame([(f"{str(feature['properties']['STATE']).zfill(2)}{str(feature['properties']['COUNTY']).zfill(3)}", feature['properties']['NAME']) for feature in geojson_data['features']],
                      columns=['STATEFP_COUNTYFP', 'NAME'])

# change the STATEFP & COUNTYFP codes to string data so they can be concatenated
es_walk = pd.read_csv('/Users/modelnic/Python/ES-Walkability/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv')
es_walk['STATEFP'] = es_walk['STATEFP'].astype(str)
es_walk['COUNTYFP'] = es_walk['COUNTYFP'].astype(str)
es_walk['STATEFP_COUNTYFP'] = es_walk['STATEFP'].str.zfill(2) + es_walk['COUNTYFP'].str.zfill(3)
aggregated_df = es_walk.groupby(['CBSA_Name', 'STATEFP_COUNTYFP', 'STATEFP', 'COUNTYFP']).agg({
    'TotPop': 'mean',
    'CountHU': 'median',
    'HH': 'median',
    'P_WrkAge': 'mean',
    'AutoOwn0': 'median',
    'AutoOwn2p': 'median',
    'R_LowWageWk': 'median',
    'R_HiWageWk': 'median',
    'D3A': 'median',
    'D3AAO': 'median',
    'D3AMM': 'median',
    'D3APO': 'median',
    'D3B': 'median',
    'D3BAO': 'median',
    'D3BMM4': 'median',
    'D3BPO4': 'median',
    'D4A': 'median',
    'D5AR': 'median',
    'NatWalkInd': 'median',
}).reset_index()

print("Unique aggregated df values")
print(aggregated_df[['STATEFP_COUNTYFP', 'CBSA_Name']].drop_duplicates())
print("Unique geo df values")
print(geo_df[['STATEFP_COUNTYFP', 'NAME']].drop_duplicates())
es_Walk = pd.merge(aggregated_df, geo_df, on='STATEFP_COUNTYFP', how='left')

included_cols = ['NAME', 'STATEFP_COUNTYFP', 'STATEFP', 'COUNTYFP', 'TotPop', 'CountHU', 'HH', 'P_WrkAge', 'AutoOwn0', 'AutoOwn2p',
                 'R_LowWageWk', 'R_HiWageWk', 'D3A', 'D3AAO', 'D3AMM', 'D3APO', 'D3B', 'D3BAO',
                 'D3BMM4', 'D3BPO4', 'D4A', 'D5AR', 'NatWalkInd']
es_Walk = es_Walk[included_cols]
# Rename columns
es_Walk = es_Walk.rename(columns={'D3A': 'RdNetDens', 'D3AAO': 'NetDAuto', 'D3AMM': 'NetDMu',
                                  'D3APO': 'NetDPed', 'D3B': 'StDens', 'D3BAO': 'IntrDAuto',
                                  'D3BMM4': '4IntrMu', 'D3BPO4': '4IntPed', 'D4A': 'CenTTrans',
                                  'D5AR': 'Job45Dr'})
es_Walk['CountyName'] = es_Walk['NAME']
es_Walk = es_Walk.round(2)
print(es_Walk)

es_Walk.to_csv('/Users/modelnic/Python/ES-Walkability/Walk_Indexx.csv', index=False)
