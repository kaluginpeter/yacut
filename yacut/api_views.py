from http import HTTPStatus
from flask import jsonify, request

from . import app
from .constants import BASE_URL
from .models import URLMap
from .error_handlers import InvalidAPIUsage

NOT_FOUND_ERROR_MESSAGE = 'Указанный id не найден'
EMPTY_REQUEST_BODY_ERROR_MESSAGE = 'Отсутствует тело запроса'


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(
            EMPTY_REQUEST_BODY_ERROR_MESSAGE, HTTPStatus.BAD_REQUEST
        )
    url_instance = URLMap.create_short_url(
        data.get('url'),
        data.get('custom_id')
    )
    return (
        jsonify(
            {
                'url': url_instance.original,
                'short_link': BASE_URL + url_instance.short
            }
        ),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def redirect_to_original_url(short_id):
    original_url = URLMap.find_short_url_instance(short_url=short_id)
    if original_url is not None:
        return jsonify({'url': original_url.original}), HTTPStatus.OK
    raise InvalidAPIUsage(NOT_FOUND_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
