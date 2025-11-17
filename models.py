from datetime import datetime

from flask import url_for

from . import db

from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_id
from .constants import ORIGINAL_LENGTH, SHORT_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view', short_id=self.short,
                               _external=True)
        )

    @classmethod
    def get_by_short(cls, short_id):
        return cls.query.filter_by(short=short_id).first()

    @staticmethod
    def create_unique_short_url(original_url, custom_id=None):
        if custom_id:
            existing = URLMap.get_by_short(custom_id)
            if existing:
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            short_id = custom_id
        else:
            short_id = get_unique_short_id()
            while URLMap.get_by_short(short_id):
                short_id = get_unique_short_id()

        url_map = URLMap(original=original_url, short=short_id)

        db.session.add(url_map)
        db.session.commit()

        return url_map
