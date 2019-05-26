from pathlib import Path
import trafaret as t
from aiohttp import web
import yaml

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / 'config'


def load_config(config_file):

    with open(CONFIG_DIR / config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config


CONFIG = load_config('config.yml')
