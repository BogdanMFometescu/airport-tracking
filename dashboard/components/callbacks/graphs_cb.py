import os
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('API_HOST', 'localhost')

common_layout = {
    'title_font_size': 22,
    'font_family': "Lato, sans-serif",
    'font_color': "#444",
    'title_font_color': "#2b2b2b",
    'legend_title_font_color': "#2a3f5f",
    'paper_bgcolor': '#f4f4f4',
    'plot_bgcolor': '#f4f4f4',
    'legend_bgcolor': 'rgba(246, 248, 250, 0.5)',
    'xaxis': {
        'title_standoff': 10,
        'tickangle': -45,
        'tickfont_size': 14,
        'title_font': {'size': 16},
    },
    'yaxis': {
        'title_standoff': 10,
        'tickfont_size': 14,
        'title_font': {'size': 16},
    },
    'margin': {'l': 60, 'r': 30, 't': 30, 'b': 60},
    'legend': {
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1
    },
    'hovermode': 'closest',
}


def airplanes_graph(n_clicks):
    if not n_clicks:
        return px.bar()
    response = requests.get(f"http://{host}:5000/api/airplane")
    if response.status_code == 200:
        airplanes_data = response.json()
        df = pd.DataFrame(airplanes_data)
        airplane_model = df['model'].value_counts().reset_index()
        airplane_model.columns = ['Model', 'Count']
        fig = px.bar(airplane_model, x='Model', y='Count', title='Airplanes by Model', color='Model')
        fig.update_layout(**common_layout)
        return fig
    return px.bar()


def airports_graph(n_clicks):
    if not n_clicks:
        return px.bar()
    response = requests.get(f"http://{host}:5000/api/airport")
    if response.status_code == 200:
        airports_data = response.json()
        df = pd.DataFrame(airports_data)
        airports_by_country = df['country_code'].value_counts().reset_index()
        airports_by_country.columns = ['Country', 'Count']
        fig = px.bar(airports_by_country, x='Country', y='Count', title='Airports by Country',
                     color='Country')
        fig.update_layout(**common_layout)
        return fig
    return px.bar()


def schedules_graph(n_clicks):
    if not n_clicks:
        return px.bar()
    response = requests.get(f"http://{host}:5000/api/schedule")
    if response.status_code == 200:
        schedules_data = response.json()
        df = pd.DataFrame(schedules_data)
        schedules_by_status = df['status'].value_counts().reset_index()
        schedules_by_status.columns = ['Status', 'Count']
        fig = px.bar(schedules_by_status, x='Status', y='Count',
                     title='Schedule by status : active-landed-scheduled-canceled', color='Status')
        fig.update_layout(**common_layout)
        return fig
    return px.bar()
