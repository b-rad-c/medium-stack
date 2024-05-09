import os
import json
import stat
import shutil
import importlib

from pathlib import Path
from configparser import ConfigParser
from typing import Generator

from mcore.util import example_model, example_cid
from mcore.types import ContentId
from mcore.models import ContentModel

from jinja2 import Environment, FunctionLoader, StrictUndefined, UndefinedError
from pydantic import BaseModel, ValidationError
from bson import ObjectId

__all__ = [
    'MTemplateError',
    'MTemplateProject',
    'MTemplateExtractor'
]

class MTemplateError(Exception):
    pass

class SourceModel(BaseModel):
    type:str
    creator_type:str
    cid_type:str
    id_type:str

    endpoint:str | None
    db_name:str | None

    snake_case:str
    kebab_case:str
    camel_case:str
    pascal_case:str
    lower_case:str

    example_cid_hash:str
    example_cid_size:int

    @classmethod
    def from_model_type(cls, model_type:BaseModel | ContentModel) -> 'SourceModel':
        name_split = model_type.LOWER_CASE.split(' ')
        snake_case = '_'.join(name_split)
        pascal_case = ''.join([name.capitalize() for name in name_split])
        kebab_case = '-'.join(name_split)
        camel_case = pascal_case[0].lower() + pascal_case[1:]

        if pascal_case != model_type.__name__:
            raise ValueError(f'model name must be in pascal case, expected: {pascal_case} got: {model_type.__name__}')
        
        try:
            endpoint = model_type.ENDPOINT
        except AttributeError:
            endpoint = None

        try:
            db_name = model_type.DB_NAME
        except AttributeError:
            db_name = None

        cid = example_cid(model_type)

        kwargs = {
            'type': pascal_case,
            'creator_type': f'{pascal_case}Creator',
            'cid_type': f'{pascal_case}Cid',
            'id_type': f'{pascal_case}Id',

            'endpoint': endpoint,
            'db_name': db_name,

            'snake_case': snake_case,
            'kebab_case': kebab_case,
            'camel_case': camel_case,
            'pascal_case': pascal_case,
            'lower_case': model_type.LOWER_CASE,

            'example_cid_hash': cid.hash,
            'example_cid_size': cid.size,
        }
        return cls(**kwargs)


class SourceModelList:

    def __init__(self, module_name:str) -> None:
        self.module_name = module_name
        self.module = importlib.import_module(module_name)
        self.module_file = Path(self.module.__file__)
        self.models: list[SourceModel] = []
        self._load()

    def __iter__(self):
        return self.models.__iter__()
    
    def __next__(self):
        return self.models.__next__()
    
    def __len__(self):
        return self.models.__len__()

    def _load(self):
        for name in self.module.__all__:
            model = getattr(self.module, name)

            try:
                is_base_model = issubclass(model, BaseModel)
                is_content_model = issubclass(model, ContentModel)
            except TypeError:
                continue

            # print(is_base_model, is_content_model, name)

            if is_base_model and is_content_model:
                try:
                    source_model = SourceModel.from_model_type(model)
                except ValidationError as e:
                    raise ValueError(f'error creating source model from {name} | {e}')

                # verify cid type #

                try:
                    cid = getattr(self.module, source_model.cid_type)
                except AttributeError:
                    raise AttributeError(f'model {name} must havee CID defined as {source_model.cid_type}')
                
                try:
                    if not cid.__args__[0] is ContentId:
                        raise TypeError(f'{source_model.cid_type} must be ContentId')
                except IndexError:
                    raise TypeError(f'{source_model.cid_type} must be ContentId')

                # verify id type #

                try:
                    id = getattr(self.module, source_model.id_type)
                except AttributeError:
                    raise AttributeError(f'model {name} must have ID defined as {source_model.id_type}')
                
                try:
                    if not id.__args__[0] is ObjectId:
                        raise TypeError(f'{source_model.id_type} must be ObjectId')
                except IndexError:
                    raise TypeError(f'{source_model.id_type} must be ObjectId')
                
                self.models.append(source_model)

    @property
    def with_endpoint(self) -> list[SourceModel]:
        return filter(lambda model: model.endpoint is not None, self.models)
    
    @property
    def with_db(self) -> list[SourceModel]:
        return filter(lambda model: model.db_name is not None, self.models)


class MTemplateProject:

    template_root = Path(__file__).parent / 'app'

    def __init__(self, config_path:Path | str) -> None:

        # load conf #

        self.config_path = Path(config_path)
        try:
            with open(self.config_path, 'r') as f:
                self.config = ConfigParser()
                self.config.read_file(f)
        except FileNotFoundError:
            raise MTemplateError(f'Config file not found: {config_path}')
        
        # set conf attribute #

        self.models = SourceModelList(self.config['mtemplate']['models'])
        self.dist_directory = Path(self.config['mtemplate']['output'])
        self.package_name = self.config['global_template_variables']['package_name']
        self.dist_package = self.dist_directory / 'src' / self.package_name

        # jinja env #

        loader = lambda name: MTemplateExtractor.template_from_file(self.template_root / name)

        self.jinja_env = Environment(
            autoescape=False,
            loader=FunctionLoader(loader),
            undefined=StrictUndefined
        )

        try:
            self.jinja_env.globals = dict(self.config['global_template_variables'])
            self.jinja_env.globals['models'] = self.models
        except KeyError:
            raise KeyError(f'global_template_variables must be defined in mtemplate config file')
        
        required_globals = [
            'package_name',
            'env_var_prefix',
            'ops_class_name',
            'client_class_name',
            'api_prefix',
            'docker_image_tag',
            'author_name',
            'author_email',
        ]

        for required_global in required_globals:
            if not required_global in self.jinja_env.globals:
                raise KeyError(f'"{required_global}" must be defined in "global_template_variables" in mtemplate config file')
             
    def _reset_output(self):
        shutil.rmtree(self.dist_directory, ignore_errors=True)
    
    def _output_file(self, path:Path, output:str):
        os.makedirs(path.parent, exist_ok=True)

        with open(path, 'w+') as f:
            f.write(output)

    def _file_ls(self, path:Path):
        for entry in os.scandir(path):
            if entry.is_file():
                if entry.name == '.DS_Store':
                    continue
                yield Path(entry.path).relative_to(self.template_root)

    def template_files(self) -> Generator[Path, None, None]:
        template_dirs = [
            self.template_root,
            self.template_root / 'src' / 'sample_app',
            self.template_root / 'tests',
            self.template_root / 'tests' / 'mcore',
            self.template_root / 'tests' / 'sample_app',
        ]

        # models file should be ignored bc its not a template, 
        # it will be replaced by the useres models file
        ignore = Path('src/sample_app/models.py')

        for template_dir in template_dirs:
            for entry in self._file_ls(template_dir):
                if entry != ignore:
                    yield entry
    
    def binary_files(self):
        yield from self._file_ls(self.template_root / 'tests' / 'samples')

    def render(self, debug:bool=False):
        self._reset_output()

        # copy source models file #

        models_file_src = self.models.module_file
        models_file_dest = self.dist_package / models_file_src.name

        os.makedirs(models_file_dest.parent, exist_ok=True)
        shutil.copy(models_file_src, models_file_dest)

        # render template files #

        for template_file in self.template_files():
            template_src_path = self.template_root / template_file

            replaced_path = Path(template_file.as_posix().replace('sample_app', self.package_name))
            template_out_path = self.dist_directory / replaced_path
            
            if debug:
                debug_output_path = template_out_path.with_name(template_out_path.name + '.jinja2')
                jinja_template = MTemplateExtractor.template_from_file(template_src_path)
                self._output_file(debug_output_path, jinja_template)

            else:
                jinja_template = self.jinja_env.get_template(template_file.as_posix())
                try:
                    rendered_template = jinja_template.render()
                except UndefinedError as e:
                    raise UndefinedError(f'{e} in template {template_file}')
                
                self._output_file(template_out_path, rendered_template)

        # copy binary files #
            
        for binary_file in self.binary_files():
            src_path = self.template_root / binary_file
            out_path = self.dist_directory / binary_file
            os.makedirs(out_path.parent, exist_ok=True)
            shutil.copy(src_path, out_path)

        # make build script executable #
        
        build_script = self.dist_directory / 'build.sh'
        os.chmod(build_script, os.stat(build_script).st_mode | stat.S_IXUSR)

    
class MTemplateExtractor:

    def __init__(self, path:str|Path) -> None:
        self.path = Path(path)
        self.template = ''
        self.template_lines = []
        self.template_vars = {}

    def _parse_vars_line(self, line:str, line_no:int):
        try:
            vars_str = line.split('::')[1].strip()
            vars_decoded = json.loads(vars_str)
            if not isinstance(vars_decoded, dict):
                raise MTemplateError(f'vars must be a json object not "{type(vars_decoded).__name__}" on line {line_no}')
            
            self.template_vars.update(vars_decoded)

        except json.JSONDecodeError as e:
            raise MTemplateError(f'caught JSONDecodeError in vars definition on line {line_no} | {e}')

    def _parse_for_lines(self, definition_line:str, lines:list[str], start_line_no:int):

        # parse for loop definition #

        try:
            definition_split = definition_line.split('::')
            jinja_line = definition_split[1]

        except IndexError:
            raise MTemplateError(f'for loop definition mmissing jinja loop syntax on {start_line_no}')
        
        # parse block vars #

        try:
            block_vars = json.loads(definition_split[2].strip())
            if not isinstance(block_vars, dict):
                raise MTemplateError(f'vars must be a json object not "{type(block_vars).__name__}" on line {start_line_no}')
            
            self.template_vars.update(block_vars)

        except IndexError:
            """no vars defined for block, ignore exception"""

        except json.JSONDecodeError as e:
            raise MTemplateError(f'caught JSONDecodeError in vars definition on line {start_line_no} | {e}')
        
        # append lines to template #

        self.template_lines.append(jinja_line.strip() + '\n')

        for line in lines:
            new_line = line 
            for key, value in block_vars.items():
                new_line = new_line.replace(key, '{{ ' + value + ' }}')
            self.template_lines.append(new_line)
        
        self.template_lines.append('{% endfor %}\n')

    def create_template(self) -> str:
        template = ''.join(self.template_lines)
        for key, value in self.template_vars.items():
            template = template.replace(key, '{{ ' + value + ' }}')
        return template

    def write(self, path:str|Path):
        with open(path, 'w+') as f:
            f.write(self.create_template())

    def parse(self):

        with open(self.path, 'r') as f:
            line_no = 0

            # iter over each line of file #

            for line in f:
                line_no += 1
                line_stripped = line.strip()

                # vars line #

                if line_stripped.startswith('# vars :: '):
                    self._parse_vars_line(line_stripped, line_no)

                # for loop #

                elif line_stripped.startswith('# for :: '):
                    for_lines = []
                    start_line_no = line_no

                    while True:

                        # seek ahead to each line in for loop #

                        try:
                            next_line = next(f)
                        except StopIteration:
                            raise MTemplateError(f'Unterminated for loop starting on line {start_line_no} of {self.path}')
                        
                        next_line_strippped = next_line.strip()
                        line_no += 1
                            
                        if next_line_strippped == '# endfor ::':
                            break

                        for_lines.append(next_line)
                    
                    self._parse_for_lines(line_stripped, for_lines, start_line_no)

                # end for #
                
                elif line_stripped.startswith('# endfor ::'):
                    raise MTemplateError(f'endfor without beginning for statement on line {line_no}')
            
                else:
                    self.template_lines.append(line)
    @classmethod
    def template_from_file(cls, path:str|Path) -> str:
        instance = cls(path)
        instance.parse()
        return instance.create_template()