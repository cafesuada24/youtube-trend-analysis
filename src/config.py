from typing import Literal, TypedDict

import yaml


class AppConfig(TypedDict):
    path: dict[Literal['transcripts'], str]


def load_app_config(config_path: str = 'config/config.yaml') -> AppConfig:
    """Load the application config from a path."""
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    if 'path' not in config:
        config['path'] = {'transcripts': 'data/transcripts'}

    return config
