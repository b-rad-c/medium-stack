#!/usr/bin/env python3
import argparse
from mtemplate import *

def render(config_path:str):
    project = MTemplateProject(config_path)
    project.render()

def extract(source:str, output:str):
    extractor = MTemplateExtractor(source)
    extractor.parse()
    if output == '-':
        print(extractor.create_template())
    else:
        extractor.write(output)

#
# cli
#

parser = argparse.ArgumentParser(description='Medium Stack templating engine')
parser.add_argument('command', choices=['render', 'extract'], help='Which command to run')

_default_config_path = './mtemplate.conf'
parser.add_argument('--config', '-c', help=f'Path to project config file: {_default_config_path}', default=_default_config_path, type=str)
parser.add_argument('--source', '-s', help='Supply source path', default='.', type=str)
parser.add_argument('--output', '-o', help='Supply path for output or - for stdout', default='-', type=str)

args = parser.parse_args()

match args.command:
    case 'render':
        try:
            render(args.config)
        except MTemplateError as e:
            print(e)
            raise SystemExit(1)
    case 'extract':
        extract(args.source, args.output)
    case _:
        print('Unknown mode')
