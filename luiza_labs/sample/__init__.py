import json
from pathlib import Path


def read_sample_json(path: str):
    with open(Path(__file__).resolve().parent / path, "r") as f:
        return json.load(f)
