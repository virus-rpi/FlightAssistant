import json


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
