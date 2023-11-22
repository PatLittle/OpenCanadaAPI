#!/usr/bin/env python3

import sys
from pathlib import Path
import json
import requests

SOURCE_URL = 'https://open.canada.ca/data/api/action/scheming_dataset_schema_show?type=dataset'
LANGS = 'en', 'fr'
HERE = Path(__file__).parent

def main():
    schema = download_schema()
    for g in LANGS:
        generate_dataset_schema(g, schema)
        generate_resource_multipart_schema(g, schema)

def download_schema():
    r = requests.get(SOURCE_URL)
    envelope = r.json()
    schema = envelope['result']
    return schema


def field_schema(f, lang):
    o = {
        'type': 'string',
        'title': f['label'][lang],
        'description': f.get('help_text', {'en':'', 'fr':''})[lang],
    }
    if 'fluent_text' in f.get('validators', ''):
        o['type'] = 'object'
        o['properties'] = {
            'en': {'type': 'string'},
            'fr': {'type': 'string'},
        }
    if 'scheming_choices' in f.get('validators', '') and 'choices' in f:
        o['enum'] = [c['value'] for c in f['choices']]

    return o

def generate_dataset_schema(lang, schema):
    out_name = HERE / 'schemas' / f'dataset-{lang}.json'

    out = {
        'type': 'object',
        'properties': {
            'resources': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {},
                },
            },
        },
    }

    for f in schema['dataset_fields']:
        if 'label' not in f or f['label'].keys() != set(LANGS):
            continue
        o = field_schema(f, lang)

        out['properties'][f['field_name']] = o


    for f in schema['resource_fields']:
        if 'label' not in f or f['label'].keys() != set(LANGS):
            continue
        o = field_schema(f, lang)

        out['properties']['resources']['items']['properties'][f['field_name']] = o


    json.dump(out, open(out_name, 'w', encoding='utf-8'), indent=2)

def generate_resource_multipart_schema(lang, schema):
    out_name = HERE / 'schemas' / f'resource-multipart-{lang}.json'

    out = {
        'type': 'object',
        'properties': {
            'clear_upload': {
                'type': 'string',
                'description':
                    'Set to "true" to remove an existing uploaded file'
                    if lang == 'en' else
                    '...'
            },
            'upload': {
                'type': 'string',
                'format': 'binary',
                'description':
                    'Upload a file instead of providing a url'
                    if lang == 'en' else
                    '...'
            },
        },
    }

    for f in schema['resource_fields']:
        if 'label' not in f or f['label'].keys() != set(LANGS):
            continue
        o = field_schema(f, lang)

        out['properties'][f['field_name']] = o

    json.dump(out, open(out_name, 'w', encoding='utf-8'), indent=2)

main()
