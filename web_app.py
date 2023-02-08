from dash import Dash, html, dcc
import plotly.express as px
from utility import getData
from pandas import DataFrame
import base64
from dash.dependencies import Input, Output, State

app = Dash(__name__)

data = getData("log.txt", None)
tick_data = data.get("flight_data")


def height_plot():
    global tick_data

    heights = []
    for i in tick_data:
        heights.append(i["h"])
    deployed_ticks = []
    for i, j in enumerate(tick_data):
        if j["d"] == "1":
            deployed_ticks.append(i)
    ground_ticks = []
    for i, j in enumerate(tick_data):
        if j["s"] == 0:
            ground_ticks.append(i)
    ascent_ticks = []
    for i, j in enumerate(tick_data):
        if j["s"] == 1:
            ascent_ticks.append(i)
    descent_ticks = []
    for i, j in enumerate(tick_data):
        if j["s"] == 2:
            descent_ticks.append(i)

    fig = px.line(DataFrame(data=DataFrame({'Height [m]': heights})))
    if len(deployed_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(deployed_ticks),
            x1=max(deployed_ticks),
            y0=min(heights),
            y1=max(heights),
            fillcolor="green" if min(deployed_ticks) > 10 else "red",
            opacity=0.3,
        )
    if len(ground_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(ground_ticks),
            x1=max(ground_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="gray",
            opacity=0.3,
        )
    if len(ascent_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(ascent_ticks),
            x1=max(ascent_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="blue",
            opacity=0.3,
        )
    if len(descent_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(descent_ticks),
            x1=max(descent_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="yellow",
            opacity=0.3,
        )
    fig.update_layout(template="plotly_dark")
    return fig


def current_plot():
    global tick_data

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


def degrees_plot():
    global tick_data

    gx = []
    gy = []
    gz = []

    for i in tick_data:
        gx.append(i["gx"])
        gy.append(i["gy"])
        gz.append(i["gz"])

    return px.line(DataFrame(data=DataFrame({'gx [°]': gx, 'gy [°]': gy, 'gz [°]': gz}))).update_layout(
        template="plotly_dark")


def acceleration_plot():
    global tick_data

    ax = []
    ay = []
    az = []

    for i in tick_data:
        ax.append(i["ax"])
        ay.append(i["ay"])
        az.append(i["az"])

    return px.line(DataFrame(data=DataFrame({'ax [m/s^2]': ax, 'ay [m/s^2]': ay, 'az [m/s^2]': az}))).update_layout(
        template="plotly_dark")


def avg_tick_speed():
    global tick_data

    tick_time = []

    for i in tick_data:
        tick_time.append(i["tt"])

    avg_tick_time = (sum(tick_time) / len(tick_time))

    return str(round(avg_tick_time, 2))


app.layout = html.Div(children=[
    html.H1(children='Fight Control', style={'color': 'white'}),
    html.H2(children='General information', style={'color': 'white'}),
    html.P(children=f'Tick speed [ms]: {str(data.get("tick_speed"))} | Avg. tick calc speed [ms]: {avg_tick_speed()}',
           id="tick"),
    html.P(children=f'Open angle [°]: {data.get("open_angle")} | Close angle [°]: {data.get("close_angle")}',
           id="angle"),
    html.P(children=f'Start height [m]: {data.get("start_height")} | Deploy height [m]: {data.get("deploy_height")}',
           id="height"),
    html.P(
        children=f'Wait time [s]: {data.get("wait_time")} | {"Timer activated" if data.get("timer_state") else "Timer deactivated"}',
        id="time"),
    html.P(children=f'G threshold [g]: {data.get("g_threshold")}', id="top_g"),
    html.H2(children='Height', style={'color': 'white'}),
    dcc.Graph(
        id='height_graph',
        figure=height_plot()
    ),
    html.H2(children='Current', style={'color': 'white'}),
    dcc.Graph(
        id='current_graph',
        figure=current_plot()
    ),
    html.H2(children='Rotation', style={'color': 'white'}),
    dcc.Graph(
        id='rot_graph',
        figure=degrees_plot()
    ),
    html.H2(children='Acceleration', style={'color': 'white'}),
    dcc.Graph(
        id='acceleration_graph',
        figure=acceleration_plot()
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


def parse_contents(contents, filename):
    global data, tick_data
    content_string = contents.split(',')

    content = str(base64.b64decode(content_string[1].encode('utf-8')).decode('utf-8'))

    try:
        data = getData("", content)
        tick_data = data.get("flight_data")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.P(filename),
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename')
              )
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names)]
        return children


@app.callback(Output('tick', 'children'), Input('upload-data', 'contents'), )
def update(_):
    return f'Tick speed [ms]: {str(data.get("tick_speed"))} | Avg. tick calc speed [ms]: {avg_tick_speed()}'


@app.callback(Output('angle', 'children'), Input('upload-data', 'contents'))
def update(_):
    return f'Open angle [°]: {data.get("open_angle")} | Close angle [°]: {data.get("close_angle")}'


@app.callback(Output('height', 'children'), Input('upload-data', 'contents'))
def update(_):
    return f'Start height [m]: {data.get("start_height")} | Deploy height [m]: {data.get("deploy_height")}'


@app.callback(Output('time', 'children'), Input('upload-data', 'contents'))
def update(_):
    return f'Wait time [s]: {data.get("wait_time")} | {"Timer activated" if data.get("timer_state") else "Timer deactivated"}'


@app.callback(Output('top_g', 'children'), Input('upload-data', 'contents'))
def update(_):
    return f'G threshold [g]: {data.get("g_threshold")}'


@app.callback(Output('height_graph', 'figure'), Input('upload-data', 'contents'))
def update(_):
    return height_plot()


@app.callback(Output('current_graph', 'figure'), Input('upload-data', 'contents'))
def update(_):
    return current_plot()


@app.callback(Output('rot_graph', 'figure'), Input('upload-data', 'contents'))
def update(_):
    return degrees_plot()


@app.callback(Output('acceleration_graph', 'figure'), Input('upload-data', 'contents'))
def update(_):
    return acceleration_plot()


if __name__ == '__main__':
    app.run_server(debug=True, host="localhost")
