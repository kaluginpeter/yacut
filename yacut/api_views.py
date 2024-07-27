from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage

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
        raise InvalidAPIUsage(EMPTY_LONG_URL_ERROR_MESSAGE, 400)
    try:
        urlmap_instance = URLMap.create_short(
            data['url'],
            data.get('custom_id')
        )
    except Exception as error:
        raise InvalidAPIUsage(str(error))
    return (
        jsonify(
            {
                'url': urlmap_instance.original,
                'short_link': url_for(
                    'redirect_from_short', short=urlmap_instance.short,
                    _external=True
                )
            }
        ),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<path:short>/', methods=['GET'])
def redirect_to_original_url(short):
    urlmap_instance = URLMap.get_short_instance(short=short)
    if urlmap_instance is not None:
        return jsonify({'url': urlmap_instance.original}), HTTPStatus.OK
    raise InvalidAPIUsage(NOT_FOUND_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
