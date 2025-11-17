from flask import flash, redirect, render_template, url_for

from . import app
from .models import URLMap
from .forms import URLMapForm
from .error_handlers import InvalidAPIUsage


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_url = form.original_link.data
        custom_id = (form.custom_id.data.strip()
                     if form.custom_id.data else None)
        try:
            url_map = URLMap.create_unique_short_url(
                original_url=original_url,
                custom_id=custom_id
            )
        except InvalidAPIUsage:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('content.html', form=form)

        flash('Ваша новая ссылка готова:')
        return render_template(
            'content.html',
            form=form,
            link=url_for(
                'redirect_view',
                short_id=url_map.short,
                _external=True
            )
        )

    return render_template('content.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
