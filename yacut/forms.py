from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional, DataRequired, Length, ValidationError

from .models import URLMap


class URLForm(FlaskForm):
    original_link = StringField(
        validators=[DataRequired('Required field!'), Length(1, 256)]
    )
    custom_id = StringField(validators=[Optional(), Length(0, 16)])
    submit = SubmitField('Send')

    def validate_custom_id(self, custom_id):
        if custom_id.data and URLMap.query.filter_by(
            short=custom_id.data
        ).first():
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
