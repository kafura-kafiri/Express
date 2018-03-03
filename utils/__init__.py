from utils.pqdict import pqdict

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
    for i, key in enumerate(keys[:-1]):
        if isinstance(_dict, dict) or isinstance(_dict, pqdict):
            if key not in _dict:
                _dict[key] = [] if keys[i + 1][0].isdigit() else {}
        else:
            key = int(key)
            while len(_dict) <= key:
                _dict.append([] if keys[i + 1][0].isdigit() else {})
        _dict = _dict[key]
    if isinstance(_dict, dict):
        return _dict, keys[-1]
    key = int(keys[-1])
    while len(_dict) <= key:
        _dict.append([] if keys[i + 1][0].isdigit() else {})
    return _dict, int(keys[-1])


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
