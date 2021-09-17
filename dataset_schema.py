#!/usr/bin/env python3

import sys
from pathlib import Path
import json
import requests

SOURCE_URL = 'https://open.canada.ca/data/api/action/scheming_dataset_schema_show?type=dataset'
lang = sys.argv[1]

r = requests.get(SOURCE_URL)
envelope = r.json()
schema = envelope['result']

out = {
    'type': 'object',
    'properties': {},
}

for f in schema['dataset_fields']:
    if 'label' not in f or f['label'].keys() != {'en', 'fr'}:
        continue
    o = {
        'type': 'string',
        'title': f['label'][lang],
        'description': f.get('help_text', {'en':'', 'fr':''})[lang],
    }
    #'required': f.get('required', False),
    if 'fluent_text' in f.get('validators', ''):
        o['type'] = 'object'
        o['properties'] = {
            'en': {'type': 'string'},
            'fr': {'type': 'string'},
        }
    if 'scheming_choices' in f.get('validators', '') and 'choices' in f:
        o['enum'] = [c['value'] for c in f['choices']]

    out['properties'][f['field_name']] = o


json.dump(out, sys.stdout, indent=2)
