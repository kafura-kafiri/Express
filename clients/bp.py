from sanic import Blueprint
from sanic.response import html, json
from jinja2 import Environment, PackageLoader
import markdown
import os


bp = Blueprint('client', url_prefix='/clients')
bp.static('/static', '../clients/static')
api_env = Environment(loader=PackageLoader('clients', 'templates'))
api_env.globals['url_for'] = lambda x, y: '/clients/{}/{}'.format(x, y)
api_tmp = api_env.get_template('api/api.html')
api_md = os.path.dirname(__file__)
api_md = os.path.join(api_md, 'templates', 'api', 'api.md')
user_story_md = os.path.dirname(__file__)
user_story_md = os.path.join(user_story_md, 'templates', 'api', 'user_stories.md')


@bp.route('/API')
async def api(request):
    with open(api_md) as md:
        md = markdown.markdown(md.read())
    return html(api_tmp.render(md=md, call=True))


@bp.route('/USER_STORIES')
async def api(request):
    with open(user_story_md) as md:
        md = markdown.markdown(md.read())
    return html(api_tmp.render(md=md, call=False))


@bp.route('/test', methods=['POST', 'GET', 'DELETE', 'PUT', 'PATCH'])
async def test(request):
    print(request.form)
    print(request.args)
    print(request.method)
    return json(request)
