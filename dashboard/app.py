
import dash
from dash import html, dcc
from components.callbacks.register_callbacks import register_callbacks
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
    dcc.Input(id='dep-iata-input', type='text', placeholder='Enter IATA code to search for airport ',
              className='input-text'),
    html.Button('Search Airport Schedule', id='search-schedule-btn', className='button', n_clicks=0),
    dcc.Input(id='iata-input', type='text', placeholder='Enter IATA Code to search for airport schedule',
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

register_callbacks(app)
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
