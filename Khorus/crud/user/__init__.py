from Khorus.Choori.mongo import Bingo
from Khorus.Choori.decorators import privileges, retrieve
from Khorus.config import user as config, crud_path
from temp import users as cached_users
import os
from sanic import Blueprint
from sanic.response import json
from Khorus.crud import prime
import datetime

bp = Blueprint(config['name'], url_prefix=config['path'])
users = config['collection']['obj'] = Bingo()


@bp.listener('before_server_start')
async def init(sanic, loop):
    _users = await users.find([], {}, {
        'privileges.porter': {'$exists': True}
    })
    for user in _users:
        cached_users.sync(user['username'], user)


@bp.route('/init'.format(), methods=['POST', ])
@privileges()
@retrieve(
    '<str:form:username>', 
    '<str:form:password>', 
    '<str:form:first_name>', 
    '<str:form:last_name>', 
    '<str:form:cellphone>', 
)
async def new_user(request, payload, username, password, first_name, last_name, cellphone, ):
    
    options = []
    
    d = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "cellphone": cellphone,
        "salt": "",
        "privileges": {},
        "bank": {
            "name": "",
            "account": "",
            "fee_per_order": "",
            "fixed_salary": ""
        },
        "detail": {
            "probation": "",
            "melli_code": "",
            "birth_date": "",
            "sheba": ""
        }
    }
    
    return json(await users.insert(options, payload, d, ))


@bp.route('/<username>/add-privilege:<privilege>', methods=['POST', ])
@privileges('zoodfood', 'dev', )
@retrieve()
async def add_privilege(request, payload, privilege, username, ):
    
    options = []
    
    query = {
        "username": username
    }
    
    node = "privileges.{privilege}".format(privilege=privilege)
    
    d = {
        "status": "",
        "shift": {}
    }
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))


@bp.route('/@status:<{status}>'.format(status='status', ), methods=['POST', ])
@privileges('porter', )
@retrieve(
)
async def update_status(request, payload, status, ):
    
    options = [
        "--me"
    ]
    
    query = {}
    
    node = "privileges.porter.status"
    
    d = int(status)
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))


@bp.route('/@shift:<{shift}>=<{head}>,<{tail}>'.format(shift='shift', head='head', tail='tail'), methods=['POST', ])
@privileges('porter', )
@retrieve(
)
async def update_shift(request, payload, shift, head, tail, ):
    
    options = [
        "--me"
    ]
    
    query = {}
    
    node = "privileges.porter.shift.{shift}".format(shift=shift)
    
    d = [int(head), int(tail)]
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))


#  manual
@bp.route('/frees', methods=["POST"])
@privileges('khorus', 'dev', 'operator')
async def frees(request, payload, ):
    now = datetime.datetime.now()
    now = now.hour * 3600 + now.minute * 60 + now.second
    now = 4
    params = [
        {
            "$match": {
                "$and": [
                    {
                        "privileges.porter.status": 1
                    }, {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "privileges.porter.shift.lunch.0": {
                                            "$lte": now,
                                        },
                                    }, {
                                        "privileges.porter.shift.lunch.1": {
                                            "$gt": now
                                        }
                                    },
                                ]
                            }, {
                                "$and": [
                                    {
                                        "privileges.porter.shift.dinner.0": {
                                            "$lte": now,
                                        },
                                    }, {
                                        "privileges.porter.shift.dinner.1": {
                                            "$gt": now
                                        }
                                    },
                                ]
                            }
                        ]
                    },
                ]
            }
        }, {
            "$lookup": {
                "from": "orders",
                "let": {
                    "porter": "$username"
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$ne": ["$status", "delivered"]},
                                    {"$ne": ["$username", "$$porter"]}
                                ],
                            }
                        }
                    },
                    {
                        "$group": {
                            "busies": {
                                "$addToSet": "$username"
                            },
                            "_id": "$$porter"
                        }
                    },
                ],
                "as": "orders"
            }
        }, {
            "$match": {
                "orders.0.busies": {"$ne": []}
            }
        }, {
            "$lookup": {
                "from": "locations",
                "let": {
                    "porter": "$username"
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$username", "$$porter"]}
                                ]
                            }
                        },
                    }, {
                        "$sort": {
                            "_date": -1
                        }
                    }, {
                        "$limit": 1
                    }
                ],
                "as": "location"
            }
        }
    ]
    _users = await users.collection.aggregate(params).to_list(None)
    return json(_users)

import Khorus.crud.user.crud
import Khorus.crud.user.ancillary