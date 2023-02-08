import json


class getData:
    def __init__(self, path: str) -> None:
        with open(path, 'rb') as f:
            raw_data = f.read().decode('UTF-8').replace('\n', '')
            self.data = json.loads(raw_data)

    def get(self, key: str):
        return self.data[key]


if __name__ == '__main__':
    data = getData("log1.txt")
    print(data.get("tick_speed"))
