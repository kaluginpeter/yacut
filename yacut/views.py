from http import HTTPStatus
from flask import render_template, abort, redirect, url_for

from . import app
from .forms import URLForm
from .models import URLMap

NOT_FOUND_ERROR_MESSAGE = 'Страница не найдена!'


@app.route('/', methods=['GET', 'POST'])
def main_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form, short_url=None)
    try:
        url_instance = URLMap.create_short(
            form.original_link.data,
            form.custom_id.data
        )
    except Exception:
        abort(500)
    return render_template(
        'index.html', form=form, short=url_for(
            'redirect_from_short', short=url_instance.short,
            _external=True
        )
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_from_short(short):
    urlmap_instance = URLMap.get_short_instance(short)
    if urlmap_instance:
        return redirect(urlmap_instance.original)
    raise abort(HTTPStatus.NOT_FOUND, NOT_FOUND_ERROR_MESSAGE)
