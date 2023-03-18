# -*- coding: utf-8 -*-
import json
from pathlib import Path

_APP_PATH = Path(__file__).parent.parent
_CONFIG_FILE_PATH = _APP_PATH.joinpath('config.json')


def _parse_config_key(confing_data: dict, key:str, value):
    key_parts = key.split('|')
    for key_part in key_parts:
        confing_data[key_part] = {
            "url": value,
            "cache": []
        }


def parse_config() -> dict:
    if not _CONFIG_FILE_PATH.exists():
        print("The config file does not exist.")
        exit(-1)

    data = {}
    with open(_CONFIG_FILE_PATH, 'r') as f:
        for key, value in json.load(f).items():
            _parse_config_key(data, key, value)

    return data
