import simulation_component
import dash

app = dash.Dash(__name__)

app.layout = simulation_component.SimulationComponent(tick_data={})


if __name__ == '__main__':
    app.run_server(debug=True)
