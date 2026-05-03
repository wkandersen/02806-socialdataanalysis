import requests
import plotly.express as px
import plotly.graph_objects as go
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

df = pd.read_csv("./project3/data/sociodata.csv")
name_fixes = {
    "MONTCLAIRE": "MONTCLARE",
    "WASHINGTON HEIGHT": "WASHINGTON HEIGHTS",
    "O'HARE": "OHARE",
}
df["COMMUNITY AREA NAME"] = df["COMMUNITY AREA NAME"].str.upper().replace(name_fixes)
df = df[df["COMMUNITY AREA NAME"] != "CHICAGO"]
df.head()

plot_data = df.copy()


def plot_income_choropleth(col: str, filename: str):
    fig = go.Figure(
        data=px.choropleth_map(
            plot_data,
            geojson=geojson,
            locations="COMMUNITY AREA NAME",
            color=col,
            featureidkey="properties.community",
            color_continuous_scale="Magma",
            map_style="carto-positron",
            zoom=9,
            center={"lat": 41.8781, "lon": -87.6298},
            opacity=0.6,
        )
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.write_html(f"./docs/figures/{filename}", include_plotlyjs="cdn")


if __name__ == "__main__":
    plot_income_choropleth("HARDSHIP INDEX", "hardship_choropleth.html")
    plot_income_choropleth("PER CAPITA INCOME ", "income_choropleth.html")
    plot_income_choropleth(
        "PERCENT HOUSEHOLDS BELOW POVERTY", "poverty_choropleth.html"
    )
    plot_income_choropleth(
        "PERCENT AGED 16+ UNEMPLOYED", "unemployment_choropleth.html"
    )
