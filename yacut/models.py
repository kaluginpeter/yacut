from datetime import datetime
from random import randint
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
                constants.VALID_SIMBOLS_RANGE[
                    randint(0, len(constants.VALID_SIMBOLS_RANGE) - 1)
                ] for _ in range(
                    constants.SHORT_GENERATION_LENGTH
                )
            )
            if not URLMap.get_short_instance(short):
                return short

    @staticmethod
    def get_short_instance(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_short(url=None, short=None):
        if len(url) > constants.ORIGINAL_LINK_LENGTH:
            raise Exception(INVALID_LENGTH_ORIGINAL_URL_ERROR_MESSAGE)
        if short:
            if not (
                len(short) <= constants.SHORT_LENGTH and
                fullmatch(constants.REGEX_SHORT_VALIDATION, short)
            ):
                raise Exception(
                    INVALID_SHORT_ERROR_MESSAGE
                )
            if URLMap.get_short_instance(short):
                raise Exception(
                    EXISTING_SHORT_ERROR_MESSAGE
                )
        else:
            short = URLMap.gen_unique_short()

        urlmap_instance = URLMap(original=url, short=short)
        db.session.add(urlmap_instance)
        db.session.commit()
        return urlmap_instance
