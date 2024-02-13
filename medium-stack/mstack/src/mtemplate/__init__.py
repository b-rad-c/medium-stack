import os
import importlib

from pathlib import Path
from configparser import ConfigParser

from mcore.types import ContentId
from mcore.models import ContentModel

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel
from bson import ObjectId

__all__ = [
    'MTemplateProject'
]

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
        self.module = importlib.import_module(module_name)
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

    def __init__(self, config_path:Path | str) -> None:
        self.config_path = Path(config_path)
        with open(self.config_path, 'r') as f:
            self.config = ConfigParser()
            self.config.read_file(f)

        self.models = SourceModelList(self.config['mtemplate']['models'])
        self.dist_directory = Path(self.config['mtemplate']['output'])

        self.jinja_env = Environment(
            autoescape=False,
            loader=PackageLoader('mtemplate', 'templates')
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
    
    
    def _output_file(self, name:str, output:str):
        output_path = self.dist_directory / name
        os.makedirs(output_path.parent, exist_ok=True)

        with open(output_path, 'w+') as f:
            f.write(output)

    def render_client(self):
        template = self.jinja_env.get_template('client.py.jinja2')
        output = template.render(models=self.models.with_db())
        self._output_file('client.py', output)

    def render_sdk(self):
        template = self.jinja_env.get_template('sdk.py.jinja2')
        output = template.render(models=self.models.with_endpoint())
        self._output_file('sdk.py', output)

    def render(self):
        self.render_client()
        self.render_sdk()
