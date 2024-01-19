import base64
import json
from dash import html


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
