import dash
from .airports_cb import update_airport_callback, update_airports_callback
from .schedule_cb import update_schedule_callback, update_schedules_callback
from .airplane_cb import update_airplanes_callback
from .graphs_cb import airplanes_graph, schedules_graph, airports_graph


from dash.dependencies import Input, Output, State


def register_callbacks(app):
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

    @app.callback(
        Output('output-container', 'children', allow_duplicate=True),
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
        print(f"Button ID: {button_id}")
        print(f"Searching for IATA Code: {iata_code}")
        print(f"Button clicked: {button_id}")
        print(f"Dep IATA: {dep_iata}")
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
