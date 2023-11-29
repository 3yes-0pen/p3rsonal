import folium
import requests
import pandas as pd
import math
from shapely.geometry import Polygon, Point

def create_marker(location, popup_content, color):
    return folium.Marker(
        location=location,
        popup=folium.Popup(popup_content),
        icon=folium.Icon(color=color),
        min_zoom=8
    )

county_data = pd.read_csv('Walk_Indexx.csv')
geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
geojson_data = requests.get(geojson_url).json()

m = folium.Map([43, -100], zoom_start=4)

if isinstance(geojson_data, dict):
    folium.GeoJson(geojson_data).add_to(m)
    print("GeoJSON added to map")
else:
    print("The GeoJSON data is not a dictionary.")

# Extract the last 5 characters of "GEO_ID" in GeoJSON data for each feature
id_list = [feature['properties']['GEO_ID'][-5:] for feature in geojson_data['features']]
for i, feature in enumerate(geojson_data['features']):
    feature['id'] = id_list[i]
    # Set the popup content for each feature
    matching_rows = county_data.loc[county_data['STATEFP_COUNTYFP'] == int(feature['id'])]
    if not matching_rows.empty:
        feature['properties']['popup_content'] = f"{feature['properties']['NAME']} - Walkability Index: {matching_rows['NatWalkInd'].values[0]}"
    else:
        feature['properties']['popup_content'] = f"No data available for {feature['properties']['NAME']}"

# Create Choropleth layer
folium.Choropleth(
    geo_data=geojson_data,
    fill_opacity=0.70,
    line_weight=0.90,
    data=county_data,
    columns=["STATEFP_COUNTYFP", "NatWalkInd"],
    key_on="feature.id",
    fill_color="YlGn",
    threshold_scale=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    legend_name="Walkability Index",
    highlight=True,
    popup=folium.features.GeoJsonPopup(
        fields=["NAME", "NatWalkInd"],
        aliases=["County Name", "Walkability Index"],
        localize=True,
        sticky=False,
        labels=True,
        style="background-color: yellow;",
    ),
).add_to(m)

# Add GeoJson layer with popups
geojson_layer = next(filter(lambda item: isinstance(item, folium.GeoJson), m._children.values()))
for feature in geojson_layer.data['features']:
    popup_content = feature['properties']['popup_content']
    folium.GeoJson(feature, popup=folium.Popup(popup_content)).add_to(m)
    print(f"Popup content for {feature['id']}: {popup_content}")

# Create a FeatureGroup for markers
marker_group = folium.FeatureGroup(name='Markers').add_to(m)

# Add markers
num_markers = 7
for i, row in county_data.iterrows():
    county_geojson = next((feature for feature in geojson_data['features'] if feature['id'] == f"{row['STATEFP']}{row['COUNTYFP']}"), None)
    if county_geojson:
        polygon_coordinates = county_geojson['geometry']['coordinates'][0]
        flat_coordinates = [coord for sublist in polygon_coordinates for coord in sublist]
        # Ensure that there are pairs of coordinates (x, y)
        flat_coordinates = [coord for coord in flat_coordinates if isinstance(coord, (int, float))]
        if not flat_coordinates:
            continue
        if flat_coordinates:
            polygon = Polygon(zip(flat_coordinates[::2], flat_coordinates[1::2]))
            centroid = Point([polygon.centroid.x, polygon.centroid.y])
            offset_distance = 0.05
            angle_increment_c = 90
            angle_increment_p = 45
            for j in range(num_markers):
                angle_c = math.radians(j * angle_increment_c)
                angle_p = math.radians(j * angle_increment_p)
                marker_location_c = [centroid.x + offset_distance * math.sin(angle_c),
                                    centroid.y + offset_distance * math.cos(angle_c)]
                marker_popup_c = f"{row['NAME']} - Households owning 2+ cars: {row['AutoOwn2p']}, Intersection density being cars: {row['IntrDAuto']}, Time spent driving to work if drive is 45min at least: {row['Job45Dr']}, Intersection density of Pedestrians only: {row['4IntPed']}"
                
                create_marker(marker_location_c, marker_popup_c, color="orange").add_to(marker_group)

                if j % 2 == 0:
                    marker_location_p = [centroid.x + offset_distance * math.sin(angle_p),
                                        centroid.y + offset_distance * math.cos(angle_p)]
                    marker_popup_p = f"{row['NAME']} - Households owning 0 cars: {row['AutoOwn0']}, Center of county to transit: {row['CenTTrans']}, Walkability Index: {row['NatWalkInd']}, Intersection density of both Vehicles and Pedestrians: {row['4IntrMu']}"
                    create_marker(marker_location_p, marker_popup_p, color="lightblue").add_to(marker_group)

folium.LayerControl().add_to(m)

m.save("v9.html")
