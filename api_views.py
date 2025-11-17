import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_by_short(short_id)
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    url = data.get('url')
    custom_id = data.get('custom_id')

    if url is None:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if not custom_id:
        custom_id = get_unique_short_id()

    if not re.match(r'^[a-zA-Z0-9]{1,16}$', custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map = URLMap.create_unique_short_url(url, custom_id)

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
