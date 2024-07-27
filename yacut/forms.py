from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    Optional, DataRequired, Length, ValidationError, Regexp
)

from . import constants
from .models import URLMap

REQUIRED_DATA_MESSAGE = '"{0}" - this field is required!'
SUBMIT_FIELD_MESSAGE = 'Send'
EXISTING_SHORT_URL_ERROR = (
    'Предложенный вариант'
    ' короткой ссылки уже существует.'
)
INVALID_SIMBOLS_ERROR = 'Допустим только набор(A-Za-z0-9)'


class URLForm(FlaskForm):
    original_link = StringField(
        validators=[
            DataRequired(REQUIRED_DATA_MESSAGE.format('original_link')),
            Length(max=constants.ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        validators=[
            Optional(),
            Length(max=constants.SHORT_LINK_LENGTH),
            Regexp(constants.REGEX_SHORT_URL_VALIDATION)
        ]
    )
    submit = SubmitField(SUBMIT_FIELD_MESSAGE)

    def validate_custom_id(self, custom_id):
        if custom_id.data:
            if URLMap.find_short_url_instance(
                custom_id.data
            ):
                raise ValidationError(
                    EXISTING_SHORT_URL_ERROR
                )
            if not URLMap.validate_short_url(custom_id.data):
                raise ValidationError(INVALID_SIMBOLS_ERROR)
