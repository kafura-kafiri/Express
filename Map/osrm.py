import os
from datetime import datetime
import ujson as json
from jinja2 import Environment, FileSystemLoader
import urllib.request
import subprocess
import time

icon_url = 'https://developer.accuweather.com/weather-icons'
weather_weight = {i: i for i in range(45)}
weather_url = 'http://dataservice.accuweather.com/currentconditions/v1/210841?apikey=qBna6Ey7vyDqxBDsMvSqQQshrIimoKOc'
osrm_dir = os.path.join('/home/pouria', 'OSRM', 'osrm-backend')


def run_osrm(port):
    subprocess.Popen("cd {}".format(osrm_dir), cwd="/", shell=True)
    weather = {
        'WeatherText': 'Partly sunny',
        'WeatherIcon': 3,
        'IsDayTime': True,
        'Temperature': {
            'Metric': {'Value': 12.8, 'Unit': 'C', 'UnitType': 17},
            'Imperial': {'Value': 55.0, 'Unit': 'F', 'UnitType': 18}
        }
    }
    # todo clear comment
    # with urllib.request.urlopen(weather_url) as html:
    #     weather = json.loads(html.read())
    #     weather = weather[0]
    weather['hour'] = datetime.now().hour
    self_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(self_dir), trim_blocks=True)
    # with open(os.path.join(osrm_dir, 'profiles', 'car.lua'), 'w+') as f:
    #    f.write(j2_env.get_template('car.lua.jinja').render(weather=weather))
    subprocess.call(['osrm-extract ../map.osm -p profiles/car.lua'], cwd=osrm_dir, shell=True)
    subprocess.call(['osrm-contract ../map.osrm'], cwd=osrm_dir, shell=True)
    subprocess.call(['osrm-customize ../map.osrm'], cwd=osrm_dir, shell=True)
    p = subprocess.Popen(['osrm-routed ../map.osrm --algorithm=MLD --port={}'.format(port)], cwd=osrm_dir, shell=True)
    # p = subprocess.call(['osrm-extract ../map.osm'], cwd=osrm_dir, shell=True)
    # p = subprocess.call(['osrm-partition ../map.osm'], cwd=osrm_dir, shell=True)
    # p = subprocess.call(['osrm-customize ../map.osm'], cwd=osrm_dir, shell=True)
    # p = subprocess.call(['osrm-customize ../map.osm'], cwd=osrm_dir, shell=True)
    # p = subprocess.Popen(['osrm-routed --algorithm=MLD ../map.osrm --port={}'.format(port)], cwd=osrm_dir, shell=True)
    return p


