import json 
import importlib

from pathlib import Path

from mcore.models import ContentModel

from jinja2 import Environment, Template, FileSystemLoader
from pydantic import BaseModel

__all__ = [
    'PYTHON_SOURCES',
    'TEMPLATE_FOLDER',
    'OUTPUT_FOLDER',
    'jinja_env',
    'write_output',
    'extract_template',
    'loader'
]

MEDIUM_TEMPLATE_ROOT = Path(__file__).parent.parent.parent.parent
PYTHON_SOURCES = MEDIUM_TEMPLATE_ROOT / 'py'
TEMPLATE_FOLDER = MEDIUM_TEMPLATE_ROOT / 'templates'
OUTPUT_FOLDER = MEDIUM_TEMPLATE_ROOT / 'output'

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


def loader(module_name:Path | str):
    module = importlib.import_module(module_name)
    count = 0
    for name in module.__all__:
        model = getattr(module, name)

        try:
            is_base_model = issubclass(model, BaseModel)
            is_content_model = issubclass(model, ContentModel)
        except TypeError:
            continue

        print(is_base_model, is_content_model, name)

        count += 1

    print(f'{module.__file__=}')
    print(f'{len(module.__all__)=}')
    print(f'{count=}')