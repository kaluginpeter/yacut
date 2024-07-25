from datetime import datetime

from . import db


class URLMap(db.Model):
    __tablename__ = 'url_map'
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    __table_args__ = (
        db.UniqueConstraint('short', name='uq_short_url'),
    )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
