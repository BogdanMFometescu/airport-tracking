import os
import requests

from dash import html
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('API_HOST', 'localhost')


def update_airports_callback(n_clicks):
    n_clicks = int(n_clicks) if n_clicks is not None else 0
    if n_clicks < 1:
        return 'Click the button below to list airports'
    response = requests.get(f"http://{host}:5000/api/airport")
    if response.status_code == 200:
        airports = response.json()
        if airports:
            return generate_airports_html_table(airports)
        else:
            return 'No airports found'
    else:
        return 'Failed to fetch airports'


def update_airport_callback(n_clicks, iata_code):
    n_clicks = int(n_clicks) if n_clicks is not None else 0
    if n_clicks < 1:
        return 'Click the button below to list airports'
    response = requests.get(f"http://{host}:5000/api/airport/{iata_code}")
    if response.status_code == 200:
        airports = response.json()
        if airports:
            return generate_airports_html_table(airports)
        else:
            return 'No airports found'
    else:
        return 'Invalid IATA code'


def generate_airports_html_table(airports):
    if not airports:
        return "No airport data available."

    table_header = html.Thead(html.Tr([
        html.Th('Id'), html.Th('Name'), html.Th('Iata Code'), html.Th('Icao Code'),
        html.Th('Latitude'), html.Th('Longitude'), html.Th('Country code'),
    ]))
    table_rows = []
    for airport in airports:
        row = html.Tr([
            html.Td(str(airport['id'])),
            html.Td(airport['name']),
            html.Td(str(airport['iata_code'])),
            html.Td(str(airport['icao_code'])),
            html.Td(str(airport['lat'])),
            html.Td(str(airport['lng'])),
            html.Td(airport['country_code']),
        ])
        table_rows.append(row)
    table_body = html.Tbody(table_rows)
    table_title = html.H3('AIRPORTS')

    return html.Div([table_title, html.Table([table_header, table_body], className="table")])
