from flask import render_template, abort, redirect

from . import app, db
from .forms import URLForm
from .models import URLMap
from .hashing import Snowflake
from .constants import DOMAIN, HTTP_SOURCE


def gen_unique_short_id():
    snowflake = Snowflake(datacenter_id=1, worker_id=1)
    return snowflake.generate_id()


@app.route('/', methods=['GET', 'POST'])
def main_view():
    form = URLForm()
    short_url = None
    if form.validate_on_submit():
        if form.custom_id.data:
            short_url = form.custom_id.data
        else:
            short_url = gen_unique_short_id()
        url_instance = URLMap(
            original=form.original_link.data,
            short=short_url
        )
        short_url = f'{HTTP_SOURCE}://{DOMAIN}/{short_url}'
        db.session.add(url_instance)
        db.session.commit()
    return render_template('main.html', form=form, short_url=short_url)


@app.route('/<string:url>', methods=['GET'])
def redirect_from_short_url(url):
    url = url.replace('http://localhost/', '')
    original_url = URLMap.query.filter_by(short=url).first()
    if original_url:
        return redirect(original_url.original)
    raise abort(404, 'Not found')