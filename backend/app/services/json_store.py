import json
from pathlib import Path
from typing import Optional


class JsonStore:
    def __init__(self, path: Optional[Path] = None):
        self.path = path or Path(__file__).resolve().parents[1] / "data" / "db.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def read(self) -> dict:
        if not self.path.exists():
            return self._initial_data()

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        base = self._initial_data()
        base.update(data)
        return base

    def write(self, data: dict) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def next_id(self, collection: str) -> int:
        data = self.read()
        values = data.get(collection, [])
        if not values:
            return 1
        return max(int(item.get("id", 0)) for item in values) + 1

    def _initial_data(self) -> dict:
        return {
            "empleados": [],
            "asistencias": [],
            "boletas": [],
            "reportes": [],
        }
