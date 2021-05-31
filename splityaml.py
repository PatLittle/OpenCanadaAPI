"""
usage:
splityaml.py openapi.yaml en openapi-en.json
splityaml.py openapi.yaml fr openapi-fr.json
"""

LANGUAGES = {'en', 'fr'}

import json
import yaml
import sys

def split(d, lng):
    if isinstance(d, dict) and d.keys() == LANGUAGES:
        return d[lng]
    if isinstance(d, dict):
        return {k: split(v, lng) for (k, v) in d.items()}
    if isinstance(d, list):
        return [split(i, lng) for i in d]
    return d

with open(sys.argv[1], encoding='utf-8') as r:
    doc = yaml.safe_load(r)

lang = sys.argv[2]
out = split(doc, lang)

with open(sys.argv[3], 'w', encoding='utf-8') as w:
    json.dump(out, w)
