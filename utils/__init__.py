def to_list(schema, prefix='', delimiter='.'):
    if not isinstance(schema, list) and not isinstance(schema, dict):
        return [(prefix, schema)]
    else:
        features = []
        for key, value in enumerate(schema) if isinstance(schema, list) else schema.items():
            features.extend(to_list(value, ((prefix + delimiter) if prefix else '') + str(key)))
        return features


def dot_notation(_dict, key):
    keys = key.split('.')
    for key in keys[:-1]:
        if key not in _dict:
            _dict[key] = {}
        _dict = _dict[key]
    return _dict, keys[-1]


if __name__ == '__main__':
    a = {
        'a': {
            'a': 'a',
            'b': [
                'a',
                {
                    'a': 'a'
                }
            ]
        },
        'b': [
            'e'
        ]
    }

    b = {
        'b': {
            'f': 2
        }
    }

    print(to_list(a))
