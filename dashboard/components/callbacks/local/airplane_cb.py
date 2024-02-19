import requests
from dash import html


def update_airplanes_callback(n_clicks):
    if n_clicks is None or n_clicks < 1:
        return 'Click the button to search an airplane'
    response = requests.get("http://localhost:5000/api/airplane")
    if response.status_code == 200:
        schedules = response.json()
        if schedules:
            return generate_airplanes_html_table(schedules)
        else:
            return 'No schedules found'
    else:
        return 'Failed to fetch schedule data'


def generate_airplanes_html_table(airplanes):
    if not airplanes:
        return "No airplane data available."
    table_header = html.Thead(html.Tr([
        html.Th('ID'), html.Th('Iata Code'), html.Th('Model'),
        html.Th('Manufacturer'),
    ]))
    table_rows = []
    for airplane in airplanes:
        row = html.Tr([
            html.Td(str(airplane['id'])),
            html.Td(str(airplane['iata'])),
            html.Td(airplane['model']),
            html.Td(airplane['manufacturer']),
        ])
        table_rows.append(row)
    table_body = html.Tbody(table_rows)
    table_title = html.H3('AIRPLANES')
    return html.Div([table_title, html.Table([table_header, table_body], className="table")])
