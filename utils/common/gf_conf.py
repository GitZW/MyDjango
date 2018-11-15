import json
from pathlib import Path
from django.conf import settings

home = str(Path.home())

with open(home + settings.CONF_FILE, 'r') as g:
    conf = json.loads(g.read())


def get_value(name):
    return conf[name]
