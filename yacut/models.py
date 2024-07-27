from datetime import datetime
from random import choice
from re import fullmatch
from string import ascii_letters, digits

from . import db, constants
from .error_handlers import InvalidAPIUsage

EMPTY_LONG_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
INVALID_SHORT_URL_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
EXISTING_SHORT_URL_ERROR_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)


def gen_unique_short_id():
    simbols_range = ascii_letters + digits
    return ''.join(choice(simbols_range) for _ in range(6))


class URLMap(db.Model):
    __tablename__ = 'url_map'
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(constants.ORIGINAL_LINK_LENGTH), nullable=False
    )
    short = db.Column(
        db.String(constants.SHORT_LINK_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @staticmethod
    def validate_short_url(short_url):
        return (
            fullmatch(constants.REGEX_SHORT_URL_VALIDATION, short_url)
            and 1 <= len(short_url) <= 16
        )

    @staticmethod
    def find_short_url_instance(short_url):
        return URLMap.query.filter_by(short=short_url).first()

    @staticmethod
    def create_short_url(url=None, short_url=None):
        if url is None:
            raise InvalidAPIUsage(EMPTY_LONG_URL_ERROR_MESSAGE, 400)
        if short_url:
            if not URLMap.validate_short_url(short_url):
                raise InvalidAPIUsage(
                    INVALID_SHORT_URL_ERROR_MESSAGE, 400
                )
            if URLMap.find_short_url_instance(short_url):
                raise InvalidAPIUsage(
                    EXISTING_SHORT_URL_ERROR_MESSAGE, 400
                )
        else:
            short_url = gen_unique_short_id()

        url_instance = URLMap(original=url, short=short_url)
        db.session.add(url_instance)
        db.session.commit()
        return url_instance
