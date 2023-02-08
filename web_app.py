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

    d = DataFrame({'Height': heights})

    df = DataFrame(data=d)

    fig = px.line(df)
    if len(deployed_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(deployed_ticks),
            x1=max(deployed_ticks),
            y0=min(heights),
            y1=max(heights),
            fillcolor="green" if min(deployed_ticks) > 10 else "red",
            opacity=0.2,
        )
    if len(ground_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(ground_ticks),
            x1=max(ground_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="gray",
            opacity=0.2,
        )
    if len(ascent_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(ascent_ticks),
            x1=max(ascent_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="blue",
            opacity=0.2,
        )
    if len(descent_ticks) > 0:
        fig.add_shape(
            type="rect",
            x0=min(descent_ticks),
            x1=max(descent_ticks),
            y0=min(heights),
            y1=max(heights) / 4,
            fillcolor="pink",
            opacity=0.2,
        )
    fig.update_layout(template="plotly_dark")
    return fig


app.layout = html.Div(children=[
    html.H1(children='Fight Control'),
    html.H2(children='Height'),
    dcc.Graph(
        id='graph',
        figure=height_plot()
    ),
    html.H2(children='Current')
])

if __name__ == '__main__':
    app.run_server(debug=True)
