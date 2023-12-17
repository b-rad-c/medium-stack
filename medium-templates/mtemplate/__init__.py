from pathlib import Path
import json 

from mtemplate import *
from jinja2 import Environment, Template, FileSystemLoader

__all__ = [
    'PYTHON_SOURCES',
    'TEMPLATE_FOLDER',
    'OUTPUT_FOLDER',
    'jinja_env',
    'write_output',
    'extract_template'
]

PYTHON_SOURCES = Path(__file__).parent.parent / 'py'
TEMPLATE_FOLDER = Path(__file__).parent.parent / 'templates'
OUTPUT_FOLDER = Path(__file__).parent.parent / 'output'

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    keep_trailing_newline=True,
    autoescape=False
)

def write_output(name:str, content:str):
    with open(OUTPUT_FOLDER / name, 'w+') as f:
        f.write(content)


def extract_template(path:Path | str) -> (str, Template):
    base = ''
    template = ''
    capturing_template = False
    capturing_template_variables = False
    with open(path, 'r') as f:
        for line in f:
            if '# extract start' in line:
                capturing_template_variables = True
                continue
            if capturing_template_variables:
                template_vars = json.loads(line.strip()[1:].strip())
                capturing_template_variables = False
                capturing_template = True
            elif capturing_template:
                template += line
            else:
                base += line
    
    for template_var, extracted_val in template_vars.items():
        template = template.replace(extracted_val, '{{ ' + template_var + ' }}')
    
    return base, jinja_env.from_string(template)
