#!/usr/bin/env python3
import argparse
from mtemplate import *

def render(config_path:str):
    project = MTemplateProject(config_path)
    project.render()

#
# cli
#

parser = argparse.ArgumentParser(description='Medium Stack templating engine')
parser.add_argument('command', choices=['render'], help='Which command to run')

_default_config_path = './mtemplate.conf'
parser.add_argument('--config', '-c', help=f'Path to project config file: {_default_config_path}', default=_default_config_path, type=str)

args = parser.parse_args()

match args.command:
    case 'render':
        try:
            render(args.config)
        except MTemplateError as e:
            print(e)
            raise SystemExit(1)
    case _:
        print('Unknown mode')
