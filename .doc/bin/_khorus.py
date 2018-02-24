from sanic import Sanic
from sanic.response import json

app = Sanic()
db = None


@app.listener('before_server_start')
def init(sanic, loop):
    global db
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_uri = "mongodb://127.0.0.1:27017/test"
    db = AsyncIOMotorClient(mongo_uri)['test']
    print(db)


@app.route('/')
async def test(request):
    collections = await db['test'].find({}).to_list(None)
    return json(collections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, workers=20)
