import json
from mcore.util import register_model_examples

model_examples = {
    # for :: {% for model in models %} :: {'{"message":"Hello World!","num":33}': 'model.json_example_creator', '{"id":null,"cid":"0AwqG1xHnZcd343P7JmO3ucjmUJ9oaB3BX70VeD_1dCo105.json","user_cid":"0KSJLki8RZh6B1rcPEyFA_XpnbMlCjPSi0tQAoU5YzpY56.json","message":"Hello World!","num":33}': 'model.json_example', 'SampleItem': 'model.type', 'SampleItemCreator': 'model.creator_type'}
    'SampleItem': json.loads('{"id":null,"cid":"0AwqG1xHnZcd343P7JmO3ucjmUJ9oaB3BX70VeD_1dCo105.json","user_cid":"0KSJLki8RZh6B1rcPEyFA_XpnbMlCjPSi0tQAoU5YzpY56.json","message":"Hello World!","num":33}'),
    'SampleItemCreator': json.loads('{"message":"Hello World!","num":33}'),
    # endfor ::
}

register_model_examples(model_examples)
