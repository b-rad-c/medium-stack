#!/usr/bin/env python3
import argparse
from mtemplate import *


models = [
    {
        'model_type': 'StillImage',
        'creator_model_type': 'StillImageCreator',
        'model_cid_type': 'StillImageCid',
        'snake_case': 'still_image',
        'lower_case': 'still image',
        'endpoint': 'mart/still-images'
    },
    {
        'model_type': 'StillImageAlbum',
        'creator_model_type': 'StillImageAlbumCreator',
        'model_cid_type': 'StillImageAlbumCid',
        'snake_case': 'still_image_album',
        'lower_case': 'still image album',
        'endpoint': 'mart/still-image-albums'
    }
]


def client():
    base, template = extract_template(PYTHON_SOURCES / 'client.py')
    for variables in models:
        base += template.render(**variables)
    write_output('client.py', base)


def sdk():
    base, template = extract_template(PYTHON_SOURCES / 'sdk.py')
    for variables in models:
        base += template.render(**variables)
    write_output('sdk.py', base)

def all():
    client()
    sdk()

#
# cli
#

parser = argparse.ArgumentParser(description='Medium Stack templating engine')
parser.add_argument('command', choices=['all', 'client', 'sdk'], help='Which command to run')
args = parser.parse_args()

match args.command:
    case 'all':
        all()

    case 'client':
        client()

    case 'sdk':
        sdk()

    case _:
        print('Unknown mode')
