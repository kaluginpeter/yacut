from datetime import datetime
from random import choices
from re import fullmatch

from . import db, constants, exceptions

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


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(constants.ORIGINAL_LINK_LENGTH), nullable=False
    )
    short = db.Column(
        db.String(constants.SHORT_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

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
        return ''.join(
            choices(
                constants.VALID_SIMBOLS_RANGE,
                k=constants.SHORT_GENERATION_LENGTH
            )
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_short(url=None, short=None, validate=True):
        if not short:
            short = URLMap.gen_unique_short()
        if validate:
            if len(url) > constants.ORIGINAL_LINK_LENGTH:
                raise exceptions.ValidationError(
                    INVALID_LENGTH_ORIGINAL_URL_ERROR_MESSAGE
                )
            if not (
                len(short) <= constants.SHORT_LENGTH and
                fullmatch(constants.REGEX_SHORT_VALIDATION, short)
            ):
                raise exceptions.ValidationError(
                    INVALID_SHORT_ERROR_MESSAGE
                )
            if URLMap.get(short):
                raise exceptions.ValidationError(
                    EXISTING_SHORT_ERROR_MESSAGE
                )

        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
