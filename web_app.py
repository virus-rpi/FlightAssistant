from dash import Dash, html, dcc
import plotly.express as px
from utility import getData
from pandas import DataFrame

app = Dash(__name__)

data = getData("log1.txt")
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
            opacity=0.9,
        )
    if len(ground_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(ground_ticks),
            x1=max(ground_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="gray",
            opacity=0.9,
        )
    if len(ascent_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(ascent_ticks),
            x1=max(ascent_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="blue",
            opacity=0.9,
        )
    if len(descent_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(descent_ticks),
            x1=max(descent_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="pink",
            opacity=0.9,
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


app.layout = html.Div(children=[
    html.H1(children='Fight Control', style={'color': 'white'}),
    html.H2(children='Height', style={'color': 'white'}),
    dcc.Graph(
        id='graph',
        figure=height_plot()
    ),
    html.H2(children='Current', style={'color': 'white'}),
    dcc.Graph(
        id='graph',
        figure=current_plot()
    ),
    html.H2(children='Rotation', style={'color': 'white'}),
    dcc.Graph(
        id='graph',
        figure=degrees_plot()
    ),
    html.H2(children='Acceleration', style={'color': 'white'}),
    dcc.Graph(
        id='graph',
        figure=acceleration_plot()
    )
],
    style={
        'backgroundColor': '#111111',
        'font-family': 'Arial',
        'textAlign': 'center',
    }
)

if __name__ == '__main__':
    app.run_server(debug=True)
