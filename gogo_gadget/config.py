import sys

import yaml


def load_config(path):
    with open(path, 'r') as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
