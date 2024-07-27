from http import HTTPStatus
from flask import render_template, abort, redirect, flash

from . import app
from .constants import BASE_URL
from .forms import URLForm
from .models import URLMap

NOT_FOUND_ERROR_MESSAGE = 'Страница не найдена!'
SUCCESSFUL_SHORT_URL_CREATION_MESSAGE = 'Пользуйтесь на здоровье!'


@app.route('/', methods=['GET', 'POST'])
def main_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form, short_url=None)
    url_instance = URLMap.create_short_url(
        form.original_link.data,
        form.custom_id.data
    )
    flash(SUCCESSFUL_SHORT_URL_CREATION_MESSAGE)
    return render_template(
        'index.html', form=form, short_url=BASE_URL + url_instance.short
    )


@app.route('/<string:url>', methods=['GET'])
def redirect_from_short_url(url):
    original_url = URLMap.find_short_url_instance(url)
    if original_url:
        return redirect(original_url.original)
    raise abort(HTTPStatus.NOT_FOUND, NOT_FOUND_ERROR_MESSAGE)
