import pandas as pd
from sodapy import Socrata
import plotly.express as px
import numpy as np
from sklearn.neighbors import BallTree, KDTree

#Get rat data from NYC open data
app_token = 'lfSmTRrlgHSIsQ1RVSq1m34A5'
client = Socrata("data.cityofnewyork.us", app_token)
client.timeout = 480
results = client.get("erm2-nwe9", where="descriptor = 'Rat Sighting'", limit=1000000)

results_df = pd.DataFrame.from_records(results)
results_df = results_df[results_df['latitude'].notna()]

#Simplify date to month + year
results_df['Date'] = pd.to_datetime(results_df['created_date']).dt.month_name().astype(str)+' '+pd.to_datetime(results_df['created_date']).dt.year.astype(str)
results_df = results_df.sort_values(by='created_date')

#Prepare lat and lon data for mapping
results_df['latitude'] = [np.float64(x) for x in results_df['latitude']]
results_df['longitude'] = [np.float64(x) for x in results_df['longitude']]

#Load MTA station location data
MTA_df = pd.read_csv('NYC_Transit_Subway_Entrance_And_Exit_Data.csv')

#Find closest MTA station
kd = KDTree(MTA_df[["Entrance Latitude", "Entrance Longitude"]].values, metric='euclidean')
distances, indices = kd.query(results_df[["latitude", "longitude"]].dropna(), k = 1)
results_df['Distance to Subway Entrance'] = distances*111111 #convert to m

#Map data
px.set_mapbox_access_token(open(".mapbox_token").read())
fig = px.scatter_mapbox(results_df,lat='latitude',lon='longitude', animation_frame="Date", animation_group='descriptor', 
    color=np.log10(results_df['Distance to Subway Entrance']), hover_data={'Date': False, 'latitude':False, 'longitude':False},
    range_color=[0,5], color_continuous_scale='armyrose'
    )
#fig.update_layout(mapbox_style="mapbox://styles/thetimeflyer/ckxaql0tm24gx15lk96bvczf5") 'Distance to Subway Entrance':False range_color=[0,0.05]

#Update animation
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 300
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 20
fig.update_layout(coloraxis_colorbar=dict(
    title="Distance to Subway Entrance",
    tickvals=[4,3,2,1,0],
    ticktext=["10km", "1km", "100m", "10m","1m"],
))
fig.update_traces(hovertemplate=None, hoverinfo='skip')
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#font = [dict(size=20)]
#sliders = [dict(currentvalue={'prefix':'','font':font})]
#fig.update_layout(sliders=sliders)

#fig.update_geos(fitbounds='locations')

fig.show()
fig.write_html("city_rats.html")

#Extra information:
avg_rat_speed  = 19.7 #cm/s

#https://data.cityofnewyork.us/resource/erm2-nwe9.json