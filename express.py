from Khorus.khorus import app
from Map.loop import osrm
from Algorithm.random import p


if __name__ == '__main__':
    osrm.start()
    p.start()
    app.run(port=5000, workers=1, debug=True)
    osrm.join()
