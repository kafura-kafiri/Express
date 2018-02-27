from sanic.response import json
from Khorus.Choori.decorators import extract_options, privileges, retrieve
from Khorus.Choori.utils import render
from copy import deepcopy
from utils import to_list, dot_notation
from bson import ObjectId

import os
import json as native_json
'''

    retrieval = to_list(schema)
    hashtags = [(feature[0], feature[1][1:]) for feature in retrieval if '#' in feature[1]]
    retrieval = ['<{key}:{type}:$form:k>'.format(key=feature[0], type=feature[1][1:])
                 for feature in retrieval if '$' in feature[1]]

    @bp.route('/', methods=['POST'])
    @bp.route('/<_id>', methods=['POST'])
    @privileges('dev', 'operator', 'applicator')
    @retrieve(
        *retrieval
    )
    async def _put(request, payload, _id=None, **kwargs):

        options = [
            "--date"
        ]

        d = deepcopy(default)
        for key, tag in hashtags:
            _d, key = dot_notation(d, key)
            _d[key] = payload[tag]

        if _id:
            d['_id'] = ObjectId(_id)

        for key, value in kwargs.items():
            _d, key = dot_notation(d, key)
            _d[key] = value
        j = json(await bingo.insert(options, payload, d, ))
        if cache:
            cache.sync(d[cache.key], d)
        return j

'''
def prime(bp, mongo, _path, config):
    def repr(config):
        from copy import deepcopy
        obj = config['collection']['obj']
        del config['collection']['obj']
        c = deepcopy(config)
        config['collection']['obj'] = obj
        return c

    def save(prime_name, parameters):
        data = {
            'ancillary': {
                'uri': {
                    'route': '',
                    'methods': [],
                },
                'method_name': '',
                'parameters': {},
                'privileges': ['dev'],
            },
            'prime': {
                'method_name': prime_name,
                'parameters': parameters,
            },
            'config': repr(config),
        }
        path = os.path.join(_path, 'symlinks')
        try:
            os.mkdir(path)
        except FileExistsError as e:
            print(e)
        except:
            return {'status': "can't create folder SYMLINK"}
        path = os.path.join(path, prime_name)
        try:
            os.mkdir(path)
        except FileExistsError as e:
            print(e)
        except:
            return {'status': "can't create folder {}".format(prime_name.upper())}
        cnt = len(os.listdir(path))
        with open(os.path.join(path, '{}.json'.format(cnt)), 'w+') as f:
            f.write(native_json.dumps(data, indent=4))
        return {'status': path}

    @bp.route('/', methods=['PUT'])
    @bp.route('/-<options>', methods=['PUT'])
    @extract_options()
    @privileges('dev')
    @retrieve(
        '<d:dict:$form:a>'
    )
    async def _put(request, payload, d, options):
        if '--symlink' not in options:
            return json(await mongo.insert(options, payload, d))
        else:
            del options['--symlink']
            params = {
                'options': options,
                'payload': payload,
                'd': d,
            }
            return json(save('insert', params))

    @bp.route('/', methods=['DELETE'])
    @bp.route('/-<options>', methods=['DELETE'])
    @extract_options()
    @privileges('dev')
    @retrieve(
        '<q:dict:$form:a>'
    )
    async def _delete(request, payload, q, options):
        if '--symlink' not in options:
            return json(await mongo.delete(options, payload, q))
        else:
            del options['--symlink']
            params = {
                'options': options,
                'payload': payload,
                'query': q,
            }
            return json(save('delete', params))

    @bp.route('/', methods=['PATCH'])
    @bp.route('/-<options>', methods=['PATCH'])
    @extract_options()
    @privileges('dev')
    @retrieve(
        '<q:dict:$form:a>',
        '<updating_json:dict:$form:a>',
    )
    async def _update(request, payload, q, updating_json, options):
        if '--symlink' not in options:
            return json(await mongo.update(options, payload, q, updating_json))
        else:
            del options['--symlink']
            params = {
                'options': options,
                'payload': payload,
                'q': q,
                'updating_json': updating_json
            }
            return json(save('update', params))

    @bp.route('/', methods=['POST'])
    @bp.route('/-<options>', methods=['POST'])
    @extract_options()
    @privileges('dev')
    @retrieve(
        '<q:dict:$form:a>',
    )
    async def _get(request, payload, q, options, **kwargs):
        if '--symlink' not in options:
            return json(await mongo.find(options, payload, q, **kwargs))
        else:
            del options['--symlink']
            params = {
                'options': options,
                'payload': payload,
                'q': q,
                **kwargs,
            }
            return json(save('find', params))

    @bp.route('/@', methods=['POST'])
    @privileges('dev')
    @retrieve(
        '<symlink:dict:$form:a>',
    )
    async def _symlink(request, payload, symlink):
        path = os.path.join(_path, '__init__.py')
        route = symlink['ancillary']['uri']['route']
        lefts = route.split('<')[1:]
        rights = [left.split('>')[0] for left in lefts]
        rights = [right.split(':')[0] for right in rights]
        symlink['ancillary']['uri']['parameters'] = rights
        with open(path, 'a') as f:
            f.write(render('primes/symlink.py.min.jinja', symlink))
        return json({'status': 'congratulations'})
