import dash
from dash import html, dcc, Input, Output, State

from components.callbacks.airports_cb import update_airport_callback, update_airports_callback
from components.callbacks.schedule_cb import update_schedule_callback, update_schedules_callback
from components.callbacks.airplane_cb import update_airplanes_callback
from components.callbacks.graphs_cb import airplanes_graph, schedules_graph, airports_graph
from components.callbacks.maps_cb import create_map

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Air Traffic Information Dashboard", style={'textAlign': 'center'}),
    html.Br(),
    html.H2('General data'),
    dcc.Dropdown(id='list-dropdown',
                 options=[
                     {'label': 'List of Airplanes', 'value': 'airplanes'},
                     {'label': 'List of Airports', 'value': 'airports'},
                     {'label': 'List of Schedules', 'value': 'schedules'},
                 ],
                 value='airports', className='dropdown'
                 ),

    html.H2('Search data'),
    html.Button('Search Airport', id='search-airport-btn', className='button', n_clicks=0),
    dcc.Input(id='iata-input', type='text', placeholder='Enter IATA Code to search for an airport',
              className='input-text'),
    html.Button('Search Airport Schedule', id='search-schedule-btn', className='button', n_clicks=0),
    dcc.Input(id='dep-iata-input', type='text', placeholder='Enter IATA code to search for airport schedule',
              className='input-text'),
    html.Br(),
    html.Div(id='output-container', className='output-container'),
    html.Br(),
    html.H2('Graphs'),
    dcc.Dropdown(id='graph-selector',
                 options=[
                     {'label': 'Airplanes', 'value': 'airplanes'},
                     {'label': 'Airports', 'value': 'airports'},
                     {'label': 'Schedules', 'value': 'schedules'},

                 ], value='airports', className='dropdown'),
    dcc.Graph(id='dynamic-graph'),
    html.H2('Map'),
    dcc.Graph(id='map', figure=create_map())

])


@app.callback(Output('output-container', 'children'),
              Input('list-dropdown', 'value'))
def update_general_info(selected_list):
    if selected_list == 'airplanes':
        return update_airplanes_callback(1)
    elif selected_list == 'airports':
        return update_airports_callback(1)
    elif selected_list == 'schedules':
        return update_schedules_callback(1)
    return {}


@app.callback(Output('output-container', 'children', allow_duplicate=True),
              [Input('search-airport-btn', 'n_clicks'),
               Input('search-schedule-btn', 'n_clicks')],
              [State('iata-input', 'value'),
               State('dep-iata-input', 'value')],
              prevent_initial_call=True)
def search_dashboard(airport_n_clicks, schedule_n_clicks, dep_iata, iata_code):
    context = dash.callback_context
    if not context.triggered:
        return "No triggered"
    button_id = context.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'search-airport-btn':
        return update_airport_callback(airport_n_clicks, iata_code)
    elif button_id == 'search-schedule-btn':
        return update_schedule_callback(schedule_n_clicks, dep_iata)


@app.callback(Output('dynamic-graph', 'figure'),
              Input('graph-selector', 'value'))
def update_graph_selector(selected_graph):
    if selected_graph == 'airplanes':
        return airplanes_graph(1)
    elif selected_graph == 'airports':
        return airports_graph(1)
    elif selected_graph == 'schedules':
        return schedules_graph(1)
    return {}


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
