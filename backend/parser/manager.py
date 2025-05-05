import json
from typing import List

COMPONENTS = {"processors": ...}


class JsonManager:
    def file_write_components(self, name: str, data: List[dict]) -> None:
        with open(name + ".json", "w") as file:
            json.dump(data, file, indent=4)

    def get_components(self, name: str) -> List[dict]:
        with open(name + ".json", "r") as file:
            return json.load(file)


if __name__ == "__main__":
    json_manager = JsonManager()
    json_manager.file_write_components(
        name="processors", data=[{"finger": 123}, {"pinger": "fdsf"}]
    )
    print(json_manager.get_components(name="processors"))
