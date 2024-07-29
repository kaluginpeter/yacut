from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import REDIRECT_SHORT_FUNCTION_NAME
from .error_handlers import InvalidAPIUsage
from .models import URLMap

NOT_FOUND_ERROR_MESSAGE = 'Указанный id не найден'
EMPTY_REQUEST_BODY_ERROR_MESSAGE = 'Отсутствует тело запроса'
EMPTY_LONG_URL_ERROR_MESSAGE = '"url" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def create_short():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(
            EMPTY_REQUEST_BODY_ERROR_MESSAGE, HTTPStatus.BAD_REQUEST
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            EMPTY_LONG_URL_ERROR_MESSAGE, HTTPStatus.BAD_REQUEST
        )
    try:
        return (
            jsonify(
                {
                    'url': data['url'],
                    'short_link': url_for(
                        REDIRECT_SHORT_FUNCTION_NAME,
                        short=URLMap.create_short(
                            data['url'], data.get('custom_id')
                        ).short,
                        _external=True
                    )
                }
            ),
            HTTPStatus.CREATED
        )
    except URLMap.ValidationError as error:
        raise InvalidAPIUsage(str(error))
    except URLMap.DataBaseCapacityError as error:
        raise InvalidAPIUsage(error, HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/api/id/<path:short>/', methods=['GET'])
def redirect_to_original_url(short):
    url_map = URLMap.get(short=short)
    if url_map is not None:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(NOT_FOUND_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
