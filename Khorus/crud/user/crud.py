from Khorus.crud.user import bp, users
from Khorus.Choori.decorators import privileges
from temp import users as users_cache
from sanic.response import json


@bp.route('/<user>/@location', methods=['GET'])
@privileges('porter', 'applicator')
async def get_location(request, payload, user, ):
    try:
        return json(users_cache.get(user)['location'])
    except:
        query = {
            "porter": user,
        }

        projection = {}

        _users = await users.collection.find(query).sort([("_date", -1)]).limit(1)
        return json(_users)
