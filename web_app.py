from dash import Dash, html, dcc
from util import get_data, parse_contents
from dash.dependencies import Input, Output, State
from components import height_plot, current_plot, degrees_plot, acceleration_plot, velocity_plot, avg_tick_speed


class WebApp:
    def __init__(self):
        external_stylesheets = ['/assets/style.css']

        self.app = Dash(assets_folder='assets', external_stylesheets=external_stylesheets)
        self.app.title = "Flight Control"

        self.data = get_data("log.txt", None)
        self.tick_data = self.data.get("flight_data")
        self.span = 20

    def run(self):
        @self.app.callback(Output('output-data-upload', 'children'),
                           Input('upload-data', 'contents'),
                           State('upload-data', 'filename'),
                           )
        def update_output(list_of_contents, list_of_names):
            if list_of_contents is not None:
                divs, self.data, self.tick_data = parse_contents(list_of_contents, list_of_names)
                children = [divs]
                return children

        @self.app.callback(Output('tick', 'children'), Input('upload-data', 'contents'), )
        def update(_):
            return f'Tick speed [ms]: {str(self.data.get("tick_speed"))} | Avg. tick calc speed [ms]: {avg_tick_speed(self.tick_data)}'

        @self.app.callback(Output('angle', 'children'), Input('upload-data', 'contents'))
        def update(_):
            return f'Open angle [°]: {self.data.get("open_angle")} | Close angle [°]: {self.data.get("close_angle")}'

        @self.app.callback(Output('height', 'children'), Input('upload-data', 'contents'))
        def update(_):
            return f'Start height [m]: {self.data.get("start_height")} | Deploy height [m]: {self.data.get("deploy_height")}'

        @self.app.callback(Output('time', 'children'), Input('upload-data', 'contents'))
        def update(_):
            return f'Wait time [s]: {self.data.get("wait_time")} | {"Timer activated" if self.data.get("timer_state") else "Timer deactivated"}'

        @self.app.callback(Output('top_g', 'children'), Input('upload-data', 'contents'))
        def update(_):
            return f'G threshold [g]: {self.data.get("g_threshold")}'

        @self.app.callback(Output('height_graph', 'figure'), Input('upload-data', 'contents'))
        def update(_):
            return height_plot(self.tick_data, self.span)

        @self.app.callback(Output('current_graph', 'figure'), Input('upload-data', 'contents'))
        def update(_):
            return current_plot(self.tick_data)

        @self.app.callback(Output('rot_graph', 'figure'), Input('upload-data', 'contents'))
        def update(_):
            return degrees_plot(self.tick_data)

        @self.app.callback(Output('acceleration_graph', 'figure'), Input('upload-data', 'contents'))
        def update(_):
            return acceleration_plot(self.tick_data)

        @self.app.callback(Output('velocity_graph', 'figure'), Input('upload-data', 'contents'))
        def update(_):
            return velocity_plot(self.tick_data, self.data, self.span)

        self.app.layout = html.Div(children=[
            html.H1(children='Fight Control'),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                className="upload",
                accept='.json,.txt',
                multiple=False
            ),
            html.P(id='output-data-upload'),
            html.H2(children='General information', style={'color': 'white'}),
            html.P(
                children=f'Tick speed [ms]: {str(self.data.get("tick_speed"))} | Avg. tick calc speed [ms]: {avg_tick_speed(self.tick_data)}',
                id="tick"),
            html.P(children=f'Open angle [°]: {self.data.get("open_angle")} | Close angle [°]: {self.data.get("close_angle")}',
                   id="angle"),
            html.P(
                children=f'Start height [m]: {self.data.get("start_height")} | Deploy height [m]: {self.data.get("deploy_height")}',
                id="height"),
            html.P(
                children=f'Wait time [s]: {self.data.get("wait_time")} | {"Timer activated" if self.data.get("timer_state") else "Timer deactivated"}',
                id="time"),
            html.P(children=f'G threshold [g]: {self.data.get("g_threshold")}', id="top_g"),
            html.H2(children='Height', style={'color': 'white'}),
            dcc.Graph(
                id='height_graph',
                figure=height_plot(self.tick_data, self.span)
            ),
            html.H2(children='Current', style={'color': 'white'}),
            dcc.Graph(
                id='current_graph',
                figure=current_plot(self.tick_data)
            ),
            html.H2(children='Rotation', style={'color': 'white'}),
            dcc.Graph(
                id='rot_graph',
                figure=degrees_plot(self.tick_data)
            ),
            html.H2(children='Acceleration', style={'color': 'white'}),
            dcc.Graph(
                id='acceleration_graph',
                figure=acceleration_plot(self.tick_data)
            ),
            html.H2(children='Velocity', style={'color': 'white'}),
            dcc.Graph(
                id='velocity_graph',
                figure=velocity_plot(self.tick_data, self.data, self.span)
            ),
        ])

        self.app.run_server(debug=True, host="localhost")


if __name__ == '__main__':
    WebApp().run()
