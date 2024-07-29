from datetime import datetime
from random import choices
from re import fullmatch

from . import db, constants

EMPTY_LONG_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
INVALID_LENGTH_ORIGINAL_URL_ERROR_MESSAGE = (
    'значение "url" превышает допустимый размер ссылки!'
)
INVALID_SHORT_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
EXISTING_SHORT_ERROR_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
DATABASE_CAPACITY_FILLED_ERROR_MESSAGE = 'Сервис перегружен данными!'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(constants.ORIGINAL_LINK_LENGTH), nullable=False
    )
    short = db.Column(
        db.String(constants.SHORT_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    class ValidationError(Exception):
        """Исключение вызывается, если данные не прошли валидацию."""

    class DataBaseCapacityError(Exception):
        """Исключение вызывается, если база данных переполнена."""

    @staticmethod
    def gen_unique_short():
        for _ in range(constants.ATTEMPS_TO_COLLISION_COUNT):
            short = ''.join(
                choices(
                    constants.VALID_SIMBOLS_RANGE,
                    k=constants.SHORT_GENERATION_LENGTH
                )
            )
            if not URLMap.get(short):
                return short
        raise URLMap.DataBaseCapacityError(
            DATABASE_CAPACITY_FILLED_ERROR_MESSAGE
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_short(url, short=None, validate=True):
        if validate:
            if len(url) > constants.ORIGINAL_LINK_LENGTH:
                raise URLMap.ValidationError(
                    INVALID_LENGTH_ORIGINAL_URL_ERROR_MESSAGE
                )
            if short and not (
                len(short) <= constants.SHORT_LENGTH and
                fullmatch(constants.REGEX_SHORT_VALIDATION, short)
            ):
                raise URLMap.ValidationError(
                    INVALID_SHORT_ERROR_MESSAGE
                )
            if short and URLMap.get(short):
                raise URLMap.ValidationError(
                    EXISTING_SHORT_ERROR_MESSAGE
                )
        if not short:
            short = URLMap.gen_unique_short()
        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
