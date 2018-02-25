from importlib import import_module
from sanic import Sanic
from Khorus.crud.user import bp as user
from Khorus.crud.user.authentication import bp as auth
from Khorus.crud.location import bp as location
from Khorus.crud.order import bp as order
from Khorus.crud.trip import bp as trip
from Khorus.crud.history import bp as history
from Khorus.crud.vehicle import bp as vehicle
from Khorus.config import setup
from clients.bp import bp as client
from Map import bp as map

app = Sanic(__name__)
setup(app)

app.blueprint(user)
app.blueprint(location)
app.blueprint(order)
app.blueprint(trip)
app.blueprint(history)
app.blueprint(auth)
app.blueprint(vehicle)
app.blueprint(client)
app.blueprint(map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, workers=1, debug=True)
