#!/usr/bin/env python3
import json

def main():
    with open('openapi.json') as f:
        openapi = json.load(f)

    total = 0
    count = 0
    types = []
    for name, schema in openapi['components']['schemas'].items():
        total += 1
        if not name.endswith('Creator'):
            continue
        print(name)
        for prop_name, prop in schema['properties'].items():
            if 'type' in prop:
                types.append(prop['type'])
                print(f'    {prop_name}: {prop["type"]}')
            if '$ref' in prop:
                print(f'    {prop_name}: {prop["$ref"]}')
                types.append(prop['$ref'])
            if 'anyOf' in prop:
                types.append('anyOf')
                print(f'    {prop_name}:')
                for any_of in prop['anyOf']:
                    if 'type' in any_of:
                        print(f'    - {any_of["type"]}')
                    if '$ref' in any_of:
                        print(f'    - {any_of["$ref"]}')

        count += 1
    print(set(types))

    print(f'{total=} {count=}')

if __name__ == '__main__':
    main()
