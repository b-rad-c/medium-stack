# vars :: {"sample_app":"package_name", "SAMP": "env_var_prefix", "SampClient": "client_class_name"}
import json
from mcore.util import register_model_examples

model_examples = {
    # for :: {% for model in models %} :: {"{\\"message\\":\\"Hello World!\\",\\"num\\":33}": "model.json_example_creator", "{\\"id\\":null,\\"cid\\":\\"0KSJLki8RZh6B1rcPEyFA_XpnbMlCjPSi0tQAoU5YzpY56.json\\",\\"user_cid\\":null,\\"message\\":\\"Hello World!\\",\\"num\\":33}": "model.json_example"}
    'SampleItem': json.loads('{"id":null,"cid":"0KSJLki8RZh6B1rcPEyFA_XpnbMlCjPSi0tQAoU5YzpY56.json","user_cid":null,"message":"Hello World!","num":33}'),
    'SampleItemCreator': json.loads('{"message":"Hello World!","num":33}'),
    # endfor ::
}

register_model_examples(model_examples)
