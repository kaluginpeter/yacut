from http import HTTPStatus

from flask import render_template, flash, redirect, url_for, abort

from . import app
from .constants import REDIRECT_SHORT_FUNCTION_NAME
from .forms import URLForm
from .models import URLMap

NOT_FOUND_ERROR_MESSAGE = 'Страница не найдена!'


@app.route('/', methods=['GET', 'POST'])
def main_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                REDIRECT_SHORT_FUNCTION_NAME,
                short=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data,
                    validate=False
                ).short,
                _external=True
            )
        )
    except URLMap.ValidationError as error:
        flash(str(error), HTTPStatus.BAD_REQUEST)
    except URLMap.DataBaseCapacityError as error:
        flash(str(error), HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/<string:short>', methods=['GET'])
def redirect_from_short(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    raise abort(HTTPStatus.NOT_FOUND, NOT_FOUND_ERROR_MESSAGE)
