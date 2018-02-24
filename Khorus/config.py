from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid, ServerSelectionTimeoutError
import asyncio
import uvloop
import os
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

crud_path = os.path.join(os.getcwd(), 'crud')
db_name = 'BLOODY_DB'
db = None


def setup(app):
    async def start(loop, db, name, indexes):
        print('connecting to mongodb! for creating collection: {}'.format(name))
        try:
            await db.create_collection(name)
        except CollectionInvalid:
            pass
        except ServerSelectionTimeoutError:
            await asyncio.sleep(0.5)
            print('trying to connect to mongodb again...')
            loop.create_task(start(loop, db))
            return

        collection = db[name]
        # Indexes are supposed to be created here
        collection.drop_indexes()
        for index in indexes:
            collection.create_index(index)
        print('connected to mongodb! {} with indexes created'.format(name))
        return collection

    @app.listener('before_server_start')
    async def init(sanic, loop):
        global db
        mongo_uri = "mongodb://127.0.0.1:27017/"
        db = AsyncIOMotorClient()[db_name]
        for _, j in globals().items():
            if type(j) is dict and 'collection' in j:
                collection = await start(loop, db, j['collection']['name'], j['collection']['indexes'])
                while 'obj' not in j['collection']:
                    await asyncio.sleep(.1)
                    print(j['collection'])
                j['collection']['obj'].collection = collection


user = {
    'name': 'user',
    'path': 'users',
    'collection': {
        'name': 'users',
        'indexes': [
            [('username', 1)]
        ]
    }
}

location = {
    'name': 'location',
    'path': 'locations',
    'collection': {
        'name': 'locations',
        'indexes': [
            [('username', 1)]
        ]
    }
}

order = {
    'name': 'order',
    'path': 'orders',
    'collection': {
        'name': 'orders',
        'indexes': [
            [('username', 1)]
        ]
    }
}

trip = {
    'name': 'trip',
    'path': 'trips',
    'collection': {
        'name': 'trips',
        'indexes': [
            [('username', 1)]
        ]
    }
}

history = {
    'name': 'history',
    'path': 'histories',
    'collection': {
        'name': 'histories',
        'indexes': [
            [('username', 1)]
        ]
    }
}

vehicle = {
    'name': 'vehicle',
    'path': 'vehicles',
    'collection': {
        'name': 'vehicles',
        'indexes': [
            [('user', 1)]
        ]
    }
}
