import logging
import sys

import yaml


def load_config(path):
    with open(str(path), 'r') as f:
        try:
            return yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            msg = "Was not able to read YAML file %s. " \
                  "This is likely a parsing error."

            logging.error(msg, path)
            logging.exception(exc)
            sys.exit(1)
