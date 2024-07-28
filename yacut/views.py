from http import HTTPStatus

from flask import render_template, abort, redirect, url_for

from . import app
from .constants import REDIRECT_SHORT_FUNCTION_NAME
from .exceptions import ValidationError
from .forms import URLForm
from .models import URLMap

NOT_FOUND_ERROR_MESSAGE = 'Страница не найдена!'


@app.route('/', methods=['GET', 'POST'])
def main_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form, short_url=None)
    try:
        url_map = URLMap.create_short(
            form.original_link.data,
            form.custom_id.data,
            validate=False
        )
    except ValidationError:
        abort(500)
    return render_template(
        'index.html', form=form, short_url=url_for(
            REDIRECT_SHORT_FUNCTION_NAME, short=url_map.short,
            _external=True
        )
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_from_short(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    raise abort(HTTPStatus.NOT_FOUND, NOT_FOUND_ERROR_MESSAGE)
