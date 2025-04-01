from numpy import convolve, ones
from pandas import DataFrame
import plotly.express as px


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

    y0 = min(heights)
    y1 = max(heights) / Y1_FACTOR

    if deployed_ticks:
        min_deployed_ticks = min(deployed_ticks)
        max_deployed_ticks = max(deployed_ticks)
        fig.add_shape(
            type="rect",
            x0=min_deployed_ticks,
            x1=max_deployed_ticks,
            y0=y0,
            y1=y1,
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
            y0=y0,
            y1=y1,
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
            y0=y0,
            y1=y1,
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
            y0=y0,
            y1=y1,
            fillcolor="yellow",
            opacity=OPACITY,
        )
    fig.update_layout(template="plotly_dark")
    return fig


def create_voltage_ranges(tick_data):
    voltage_ranges = []
    voltage_status = None
    range_start_tick = None

    for tick_index, tick in enumerate(tick_data):
        voltage_value = tick["v"]
        tick_status = "ok" if 3 <= voltage_value <= 4.2 else "bad"

        if voltage_status is None:
            voltage_status = tick_status
            range_start_tick = tick_index
        elif tick_status != voltage_status:
            voltage_ranges.append((range_start_tick - 1, tick_index, voltage_status))
            voltage_status = tick_status
            range_start_tick = tick_index

    if voltage_status is not None:
        voltage_ranges.append((range_start_tick - 1, len(tick_data), voltage_status))

    return voltage_ranges


def voltage_plot(tick_data):
    voltages = [tick["v"] for tick in tick_data]
    voltage_ranges = create_voltage_ranges(tick_data)

    fig = px.line(DataFrame(data=DataFrame({'voltages [v]': voltages})))

    y0 = min(voltages)
    y1 = max(voltages)

    for voltage_range in voltage_ranges:
        fig.add_shape(
            type="rect",
            x0=voltage_range[0],
            x1=voltage_range[1],
            y0=y0,
            y1=y1,
            fillcolor="green" if voltage_range[2] == "ok" else "red",
            opacity=0.1 if voltage_range[2] == "ok" else 0.4,
            line=dict(
                width=0,
            ),
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
