from Khorus.Choori.decorators import privileges, retrieve
from sanic.response import json
from Khorus.crud.location import bp, locations
from temp import users as cached_users

@bp.route('/<lat>,<lng>', methods=['POST', ])
@privileges('porter', 'dev', )
@retrieve(
    '<lat:num:$uri:a>',
    '<lng:num:$uri:a>',
)
async def send_location(request, payload, lat, lng, ):
    options = [
        "--bulk",
        "--date",
    ]

    d = {
        "porter": payload['username'],
        "c": [lat, lng],
        "#": []
    }

    j = json(await locations.insert(options, payload, d, ))
    cached_users.sync("{}.{}".format(payload['username'], 'location'), [lat, lng])
    return j