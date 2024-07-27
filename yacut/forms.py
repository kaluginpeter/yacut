from re import fullmatch

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    Optional, DataRequired, Length, ValidationError, Regexp
)

from . import constants
from .models import URLMap

REQUIRED_DATA_MESSAGE = '"{0}" - this field is required!'
ORIGINAL_LINK_FIELD_NAME = 'original_link'
SUBMIT_FIELD_MESSAGE = 'Send'
EXISTING_SHORT_ERROR = (
    'Предложенный вариант'
    ' короткой ссылки уже существует.'
)
INVALID_SIMBOLS_ERROR = 'Допустим только набор(A-Za-z0-9)'


class URLForm(FlaskForm):
    original_link = StringField(
        validators=[
            DataRequired(REQUIRED_DATA_MESSAGE.format(
                ORIGINAL_LINK_FIELD_NAME
            )),
            Length(max=constants.ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        validators=[
            Optional(),
            Length(max=constants.SHORT_LENGTH),
            Regexp(constants.REGEX_SHORT_VALIDATION)
        ]
    )
    submit = SubmitField(SUBMIT_FIELD_MESSAGE)

    def validate_custom_id(self, short):
        if short.data:
            if not (
                len(short.data) <= constants.SHORT_LENGTH and
                fullmatch(constants.REGEX_SHORT_VALIDATION, short.data)
            ):
                raise ValidationError(INVALID_SIMBOLS_ERROR)
            if URLMap.get_short_instance(
                short.data
            ):
                raise ValidationError(
                    EXISTING_SHORT_ERROR
                )
