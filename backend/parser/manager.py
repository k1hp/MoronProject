import json
from typing import List

from backend.app.others.settings import DB_DIR
from backend.app.services.decorators import clear_duplicates


class JsonManager:
    def file_write_components(self, name: str, data: List[dict]) -> None:
        with open(DB_DIR / f"{name}.json", "w") as file:
            json.dump(data, file, indent=4)

    @clear_duplicates
    def get_components(self, name: str) -> List[dict]:
        with open(DB_DIR / f"{name}.json", "r") as file:
            return json.load(file)  # убирает дубликаты


if __name__ == "__main__":
    json_manager = JsonManager()
    # json_manager.file_write_components(
    #     name="tesrsfds", data=[{"finger": 123}, {"pinger": "fdsf"}]
    # )
    result = json_manager.get_components(name="processors")
    print([dict(t) for t in set(tuple(dct.items()) for dct in result)])
