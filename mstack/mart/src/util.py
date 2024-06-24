import json

mart_model_examples = {
    'Artist': json.loads('__json__'),
    'ArtistCreator': json.loads('__json__'),
}

def content_model_config(key:str) -> dict:
    try:
        return mart_model_examples[key]
    except KeyError:
        raise KeyError(f'No model example found for: {key}')
