from dash import Dash, html, dcc
import plotly.express as px
from utility import get_data
from pandas import DataFrame
import base64
from dash.dependencies import Input, Output, State
from numpy import convolve, ones


def height_plot(tick_data, span):
    heights = [i['h'] for i in tick_data]
    heights = convolve(heights, ones(span * 2 + 1) / (span * 2 + 1), mode="same")

    deployed_ticks = [i for i, j in enumerate(tick_data) if j["d"] == "1"]
    ground_ticks = [i for i, j in enumerate(tick_data) if j["s"] == 0]
    ascent_ticks = [i for i, j in enumerate(tick_data) if j["s"] == 1]
    descent_ticks = [i for i, j in enumerate(tick_data) if j["s"] == 2]

    fig = px.line(DataFrame(data=DataFrame({'Height [m]': heights})))

    OPACITY = 0.3
    Y1_FACTOR = 4

    if deployed_ticks:
        min_deployed_ticks = min(deployed_ticks)
        max_deployed_ticks = max(deployed_ticks)
        fig.add_shape(
            type="rect",
            x0=min_deployed_ticks,
            x1=max_deployed_ticks,
            y0=min(heights),
            y1=max(heights),
            fillcolor="green" if min_deployed_ticks > 10 else "red",
            opacity=OPACITY,
        )
    if ground_ticks:
        min_ground_ticks = min(ground_ticks)
        max_ground_ticks = max(ground_ticks)
        fig.add_shape(
            type="rect",
            x0=min_ground_ticks,
            x1=max_ground_ticks,
            y0=min(heights),
            y1=max(heights) / Y1_FACTOR,
            fillcolor="gray",
            opacity=OPACITY,
        )
    if ascent_ticks:
        min_ascent_ticks = min(ascent_ticks)
        max_ascent_ticks = max(ascent_ticks)
        fig.add_shape(
            type="rect",
            x0=min_ascent_ticks,
            x1=max_ascent_ticks,
            y0=min(heights),
            y1=max(heights) / Y1_FACTOR,
            fillcolor="blue",
            opacity=OPACITY,
        )
    if descent_ticks:
        min_descent_ticks = min(descent_ticks)
        max_descent_ticks = max(descent_ticks)
        fig.add_shape(
            type="rect",
            x0=min_descent_ticks,
            x1=max_descent_ticks,
            y0=min(heights),
            y1=max(heights) / Y1_FACTOR,
            fillcolor="yellow",
            opacity=OPACITY,
        )
    fig.update_layout(template="plotly_dark")
    return fig


def current_plot(tick_data):
    currents = []
    for i in tick_data:
        currents.append(i["v"])

    fig = px.line(DataFrame(data=DataFrame({'Currents [v]': currents})))

    fig.add_shape(
        type="rect",
        x0=0,
        x1=len(tick_data),
        y0=3,
        y1=4.2,
        fillcolor="green",
        opacity=0.5,
    )

    fig.update_layout(template="plotly_dark")

    return fig


def degrees_plot(tick_data):
    gx = []
    gy = []
    gz = []

    for i in tick_data:
        gx.append(i["gx"])
        gy.append(i["gy"])
        gz.append(i["gz"])

    return px.line(DataFrame(data=DataFrame({'gx [°]': gx, 'gy [°]': gy, 'gz [°]': gz}))).update_layout(
        template="plotly_dark")


def acceleration_plot(tick_data):
    ax = []
    ay = []
    az = []

    for i in tick_data:
        ax.append(i["ax"])
        ay.append(i["ay"])
        az.append(i["az"])

    return px.line(DataFrame(data=DataFrame({'ax [m/s^2]': ax, 'ay [m/s^2]': ay, 'az [m/s^2]': az}))).update_layout(
        template="plotly_dark")


def velocity_plot(tick_data, data, span):
    heights = []
    for i in tick_data:
        heights.append(i["h"])
    heights = convolve(heights, ones(span * 2 + 1) / (span * 2 + 1), mode="same")

    velocity_list = []
    v = 0
    for j, i in enumerate(heights):
        velocity_list.append(v)
        try:
            v = (heights[j + 1] - i) / (data.get("tick_speed") / 1000)
        except IndexError:
            v = velocity_list[-1]

    span_velocity = 10
    velocity_list = convolve(velocity_list, ones(span_velocity * 2 + 1) / (span_velocity * 2 + 1), mode="same")

    return px.line(DataFrame(
        data={'velocity [m/s]': velocity_list})).update_layout(
        template="plotly_dark")


def avg_tick_speed(tick_data):
    tick_time = []

    for i in tick_data:
        tick_time.append(i["tt"])

    avg_tick_time = (sum(tick_time) / len(tick_time))

    return str(round(avg_tick_time, 2))


def parse_contents(contents, filename):
    content_string = contents.split(',')

    content = str(base64.b64decode(content_string[1].encode('utf-8')).decode('utf-8'))

    try:
        data = get_data("", content)
        tick_data = data.get("flight_data")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.P(filename),
    ]), data, tick_data


class WebApp:
    def __init__(self):
        self.app = Dash(__name__)

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
            html.H1(children='Fight Control', style={'color': 'white'}),
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
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.P(id='output-data-upload'),
        ],
            style={
                'backgroundColor': '#111111',
                'font-family': 'Arial',
                'textAlign': 'center',
                'color': 'white',
            }
        )

        self.app.run_server(debug=True, host="localhost")


if __name__ == '__main__':
    WebApp().run()
