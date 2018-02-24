from Khorus.Choori.decorators import privileges, retrieve
from Khorus.crud.order import bp, orders
from sanic.response import json
import datetime


@bp.route('/unassigned'.format(), methods=['POST', ])
@privileges('dev', 'khorus', 'operator', )
@retrieve(
)
async def unassigned(request, payload, ):
    options = []

    query = {
        "username": {
            "$exists": False
        }
    }

    projection = {}

    return json(await orders.find(options, payload, query, projection, ))


@bp.route('/history-back:<{days}>'.format(days='days', ), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
)
async def history_from(request, payload, days, ):
    options = [
        "--me"
    ]

    days_ago = datetime.datetime.now() - datetime.timedelta(days=int(days))
    query = {
        "_date": {
            "$gte": days_ago
        }
    }

    group = {
        "count": {
            "$sum": 1
        },
        "year_month_day": {
            "$first": "$year_month_day"
        },
        "_id": "$year_month_day",
    }

    projection = {
        "year_month_day": {
            "$dateToString": {
                "format": "%Y-%m-%d",
                "date": "$_date"
            }
        },
        "count": {
            "$dateToString": {
                "format": "%H:%M:%S:%L",
                "date": "$_date"
            }
        }
    }

    foreign = None

    return json(await orders.aggregate(options, payload, query, group, projection, foreign, ))

