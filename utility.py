import json


class getData:
    def __init__(self, path: str, dictionary) -> None:
        if dictionary is None:
            with open(path, 'rb') as f:
                raw_data = f.read().decode('UTF-8').replace('\n', '')
        else:
            raw_data = dictionary
        self.data = json.loads(raw_data)

    def get(self, key: str):
        return self.data[key]


if __name__ == '__main__':
    data = getData("log.txt", None)
    print("Test 1: Pass" if data.get("tick_speed") == 20 else "Test 2: Fail")
