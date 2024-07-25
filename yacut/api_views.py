from flask import jsonify, request

from . import app, db
from .constants import HTTP_SOURCE, DOMAIN
from .models import URLMap
from .views import gen_unique_short_id
from .error_handlers import InvalidAPIUsage
from .utils import validate_short_url


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    if 'custom_id' in data:
        if not validate_short_url(data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400
            )
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.', 400
            )
    else:
        data['custom_id'] = gen_unique_short_id()
    short_url = f'{HTTP_SOURCE}://{DOMAIN}/{data["custom_id"]}'
    url_instance = URLMap()
    url_instance.from_dict(data)
    db.session.add(url_instance)
    db.session.commit()
    return (
        jsonify({'url': url_instance.original, 'short_link': short_url}),
        201
    )


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def redirect_to_original_url(short_id):
    short_id = short_id.replace('http://localhost/', '')
    original_url = URLMap.query.filter_by(short=short_id).first()
    if original_url is not None:
        return jsonify({'url': original_url.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
