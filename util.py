import base64
import json
from typing import List, Any
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from dash import html
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler


class get_data:
    def __init__(self, path: str, dictionary) -> None:
        if dictionary is None:
            with open(path, 'rb') as f:
                raw_data = f.read().decode('UTF-8').replace('\n', '')
        else:
            raw_data = dictionary
        self.data = json.loads(raw_data)

    def get(self, key: str):
        return self.data[key]


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


def denoise(data: list[float], window_length: int, polyorder: int) -> list[float]:
    if window_length % 2 == 0:
        window_length += 1
    return list(savgol_filter(data, window_length, polyorder))


def find_optimal_savgol_parameters(data: list[float], max_window_length: int, max_polyorder: int) -> List[Any]:
    scaler = MinMaxScaler()
    data = scaler.fit_transform(np.array(data).reshape(-1, 1)).flatten()

    train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

    min_error = float("inf")
    optimal_params = [0, 0]

    for window_length in range(3, min(max_window_length, 101), 2):  # limit max_window_length to 101
        for polyorder in range(1, min(window_length, min(max_polyorder, 5) + 1)):  # limit max_polyorder to 5
            filtered_data = denoise(data, window_length, polyorder)
            filtered_val_data = filtered_data[len(train_data):]
            error = mean_squared_error(val_data, filtered_val_data)
            if error < min_error:
                min_error = error
                optimal_params = [window_length, polyorder]

    return optimal_params
