import plotly.express as px
import pandas as pd
import requests


def create_map():
    response = requests.get("http://fastapi:5000/api/airport")
    if response.status_code == 200:
        airports = response.json()
        df = pd.DataFrame(airports)
        new_df = pd.DataFrame(
            {
                'lat': df['lat'].astype(float), 'lng': df['lng'].astype(float), 'name': df['name'].astype(str)

            })
        fig = px.scatter_mapbox(new_df, lat='lat', lon='lng', hover_name='name',
                                color_discrete_sequence=['fuchsia'], zoom=3)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
