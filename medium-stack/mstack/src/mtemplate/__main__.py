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
parser.add_argument('--config', '-c', help='Path to project config file')
args = parser.parse_args()

match args.command:
    case 'render':
        render(args.config)

    case _:
        print('Unknown mode')
