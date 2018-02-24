from sanic import Blueprint
from sanic.response import html, json
from jinja2 import Environment, PackageLoader


bp = Blueprint('client', url_prefix='/clients')
bp.static('/static', '../clients/static')
api_env = Environment(loader=PackageLoader('clients', 'templates'))
api_env.globals['url_for'] = lambda x, y: '/clients/{}/{}'.format(x, y)
api_tmp = api_env.get_template('api.html')


@bp.route('/API')
async def api(request):
    return html(api_tmp.render())


@bp.route('/test', methods=['POST', 'GET', 'DELETE', 'PUT', 'PATCH'])
async def test(request):
    print(request.form)
    print(request.args)
    print(request.method)
    return json(request)
