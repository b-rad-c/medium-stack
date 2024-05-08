import os
import json
import shutil
import importlib

from pathlib import Path
from configparser import ConfigParser
from typing import Generator

from mcore.types import ContentId
from mcore.models import ContentModel

from jinja2 import Environment, FunctionLoader
from pydantic import BaseModel
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


    @classmethod
    def from_model_type(cls, model_type:BaseModel | ContentModel) -> 'SourceModel':
        name_split = model_type.LOWER_CASE.split(' ')
        snake_case = '_'.join(name_split)
        pascal_case = ''.join([name.capitalize() for name in name_split])
        kebab_case = '-'.join(name_split)
        camel_case = pascal_case[0].lower() + pascal_case[1:]

        if pascal_case != model_type.__name__:
            raise ValueError(f'model name must be in pascal case, expected: {pascal_case} got: {model_type.__name__}')
        
        if model_type.ENDPOINT is True:
            endpoint = f'/{kebab_case}'
        elif isinstance(model_type.ENDPOINT, str):
            endpoint = model_type.ENDPOINT
        else:
            endpoint = None

        if model_type.DB is True:
            db_name = snake_case
        elif isinstance(model_type.DB, str):
            db_name = model_type.DB
        else:
            db_name = None

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
                source_model = SourceModel.from_model_type(model)

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

    def with_endpoint(self) -> list[SourceModel]:
        return filter(lambda model: model.endpoint is not None, self.models)
    
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
        package_name = self.config['global_template_variables']['package_name']
        self.dist_package = self.dist_directory / 'src' / package_name

        # jinja env #

        loader = lambda name: MTemplateExtractor.template_from_file(self.template_root / name)

        self.jinja_env = Environment(
            autoescape=False,
            loader=FunctionLoader(loader)
            # loader=PackageLoader('mtemplate', 'templates')
            # loader=FileSystemLoader(self.config_path.parent / 'templates')
        )

        try:
            self.jinja_env.globals = dict(self.config['global_template_variables'])
        except KeyError:
            raise KeyError(f'global_template_variables must be defined in mtemplate config file')
        
        if not 'env_var_prefix' in self.jinja_env.globals:
            raise KeyError(f'env_var_prefix must be defined in global_template_variables in mtemplate config file')
        
        if not 'ops_class_name' in self.jinja_env.globals:
            raise KeyError(f'ops_class_name must be defined in global_template_variables in mtemplate config file')
        
        if not 'client_class_name' in self.jinja_env.globals:
            raise KeyError(f'client_class_name must be defined in global_template_variables in mtemplate config file')
        
    def _reset_output(self):
        shutil.rmtree(self.dist_directory, ignore_errors=True)
    
    def _output_file(self, path:Path, output:str):
        os.makedirs(path.parent, exist_ok=True)

        with open(path, 'w+') as f:
            f.write(output)

    def template_files(self) -> Generator[Path, None, None]:
        template_dirs = [
            self.template_root,
            self.template_root / 'src' / 'sample_app',
        ]

        for template_dir in template_dirs:
            for path in os.scandir(template_dir):
                if path.is_file():
                    if path.name == '.DS_Store':
                        continue
                    yield Path(path.path).relative_to(self.template_root)

    def render_models(self):
        src = self.models.module_file
        shutil.copy(src, self.dist_package / src.name)

    def render_client(self):
        template = self.jinja_env.get_template('src/sample_app/client.py')
        output = template.render(models=self.models.with_db())
        self._output_file(self.dist_package / 'client.py', output)

    def render_ops(self):
        template = self.jinja_env.get_template('src/sample_app/ops.py')
        output = template.render(models=self.models.with_endpoint())
        self._output_file(self.dist_package / 'ops.py', output)

    def render_serve(self):
        template = self.jinja_env.get_template('src/sample_app/serve.py')
        output = template.render(models=self.models.with_endpoint())
        self._output_file(self.dist_package / 'serve.py', output)

    def render_pyproject_toml(self):
        template = self.jinja_env.get_template('pyproject.toml')
        output = template.render()
        self._output_file(self.dist_directory / 'pyproject.toml', output)

    def render_readme(self):
        template = self.jinja_env.get_template('README.md')
        output = template.render()
        self._output_file(self.dist_directory / 'README.md', output)

    def render_package(self):
        init_file = self.dist_package / '__init__.py'
        os.makedirs(self.dist_package, exist_ok=True)
        init_file.touch()

        self.render_pyproject_toml()
        self.render_models()
        self.render_client()
        self.render_ops()
        self.render_serve()

    def render_tests(self):
        template_test_directory = self.template_root / 'tests'
        shutil.copytree(template_test_directory, self.dist_directory / 'tests')

    def render_env(self):
        template = self.jinja_env.get_template('.env')
        output = template.render()
        self._output_file(self.dist_directory / '.env', output)

        template = self.jinja_env.get_template('.gitignore')
        output = template.render()
        self._output_file(self.dist_directory / '.gitignore', output)

    def render_dockerfiles(self):
        template = self.jinja_env.get_template('build.sh')
        output = template.render()
        self._output_file(self.dist_directory / 'build.sh', output)

        template = self.jinja_env.get_template('Dockerfile')
        output = template.render()
        self._output_file(self.dist_directory / 'Dockerfile', output)

        template = self.jinja_env.get_template('docker-compose.yml')
        output = template.render()
        self._output_file(self.dist_directory / 'docker-compose.yml', output)

        template = self.jinja_env.get_template('.dockerignore')
        output = template.render()
        self._output_file(self.dist_directory / '.dockerignore', output)

    def render_entry_scripts(self):
        # entry_py_template = self.jinja_env.get_template('entry.py')
        # entry_py_output = entry_py_template.render(models=self.models.with_endpoint())
        # self._output_file(self.dist_directory / 'entry.py', entry_py_output)

        web_sh_template = self.jinja_env.get_template('web.sh')
        web_sh_output = web_sh_template.render()
        self._output_file(self.dist_directory / 'web.sh', web_sh_output)

    def render_debug(self):
        self._reset_output()
        for path in self.template_files():
            jinja_template = MTemplateExtractor.template_from_file(self.template_root / path)
            output_path = self.dist_directory / path.with_name(path.name + '.jinja2')
            self._output_file(output_path, jinja_template)

    def render(self):
        self._reset_output()
        self.render_readme()
        self.render_package()
        self.render_tests()
        self.render_entry_scripts()
        self.render_env()
        self.render_dockerfiles()


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

                        next_line = next(f)
                        next_line_strippped = next_line.strip()
                        line_no += 1

                        if next_line == '':
                            raise MTemplateError(f'Unterminated for loop starting on line {start_line_no}')
                        
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