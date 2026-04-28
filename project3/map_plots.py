import requests
import plotly.express as px
import pandas as pd

shapefile = requests.get(
    "https://data.cityofchicago.org/resource/igwz-8jzy.json"
).json()

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": row["the_geom"],
            "properties": {k: v for k, v in row.items() if k != "the_geom"},
        }
        for row in shapefile
        if row.get("the_geom") and row["the_geom"].get("coordinates")
    ],
}

df = pd.read_csv("./data/sociodata.csv")
name_fixes = {
    "MONTCLAIRE": "MONTCLARE",
    "WASHINGTON HEIGHT": "WASHINGTON HEIGHTS",
    "O'HARE": "OHARE",
}
df["COMMUNITY AREA NAME"] = df["COMMUNITY AREA NAME"].str.upper().replace(name_fixes)
df = df[df["COMMUNITY AREA NAME"] != "CHICAGO"]
df.head()

plot_data = df.copy()

fig = px.choropleth_map(
    plot_data,
    geojson=geojson,
    locations="COMMUNITY AREA NAME",
    color="PER CAPITA INCOME ",
    featureidkey="properties.community",
    color_continuous_scale="Magma",
    map_style="carto-positron",
    zoom=9,
    center={"lat": 41.8781, "lon": -87.6298},
    opacity=0.6,
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
