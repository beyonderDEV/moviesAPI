from . import db
from . import app
import flask_whooshalchemy as wa


class Movie(db.Model):
    __searchable__ = ['title', 'description']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    description = db.Column(db.String(255))


wa.whoosh_index(app, Movie)


