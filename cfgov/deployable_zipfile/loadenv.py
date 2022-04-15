import json
import os
import sys


def loadenv():
    filename = os.path.join(sys.prefix, "../environment.json")

    if os.path.exists(filename):
        with open(filename) as f:
            os.environ.update(json.load(f))
