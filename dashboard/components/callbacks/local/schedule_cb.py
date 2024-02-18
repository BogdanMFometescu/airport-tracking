import requests
from dash import html


def update_schedules_callback(n_clicks):
    if n_clicks is None or n_clicks < 1:
        return 'Click the button ....'
    response = requests.get(f"http://fastapi:5000/api/schedule")
    if response.status_code == 200:
        schedules = response.json()
        if schedules:
            return generate_schedules_html_table(schedules)
        else:
            return 'No schedules found'
    else:
        return 'Failed to fetch schedule data'


def update_schedule_callback(n_clicks, dep_iata):
    if n_clicks is None or n_clicks < 1:
        return 'Click the button to search a schedule'
    response = requests.get(f"http://fastapi:5000/api/schedule/{dep_iata}")
    if response.status_code == 200:
        schedules = response.json()
        if schedules:
            return generate_schedules_html_table(schedules)
        else:
            return 'No schedules found'
    else:
        return 'Failed to fetch schedule data'


def generate_schedules_html_table(schedules):
    if not schedules:
        return "No schedule data available."
    table_header = html.Thead(html.Tr([
        html.Th('ID'), html.Th('Departure Time'), html.Th('Arrival Time'),
        html.Th('Status'), html.Th('Flight Number'), html.Th('Departure IATA'),
        html.Th('Arrival IATA'), html.Th('Duration')
    ]))
    table_rows = []
    for schedule in schedules:
        row = html.Tr([
            html.Td(str(schedule['id'])),
            html.Td(schedule['dep_time'].split('T')[1]),
            html.Td(schedule['arr_time'].split('T')[1]),
            html.Td(schedule['status']),
            html.Td(str(schedule['flight_number'])),
            html.Td(schedule['dep_iata']),
            html.Td(schedule['arr_iata']),
            html.Td(schedule['duration'])
        ])
        table_rows.append(row)
    table_body = html.Tbody(table_rows)
    table_title = html.H3('SCHEDULES')
    return html.Div([table_title, html.Table([table_header, table_body], className="table")])