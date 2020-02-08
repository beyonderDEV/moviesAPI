from . import db
from . import app
from . import ma
import flask_whooshalchemy as wa


class Movie(db.Model):
    __searchable__ = ['title', 'description']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    description = db.Column(db.String(255))


wa.whoosh_index(app, Movie)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(1000))


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    total_episodes = db.Column(db.Integer)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    show = db.relationship('Show', backref='seasons')


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    episode_number = db.Column(db.Integer)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    season = db.relationship('Season', backref='episodes')


class EpisodeSchema(ma.ModelSchema):
    class Meta:
        model = Episode


class SeasonSchema(ma.ModelSchema):
    class Meta:
        model = Season
    episodes = ma.Nested(EpisodeSchema, many=True)


class ShowSchema(ma.ModelSchema):
    class Meta:
        model = Show
    seasons = ma.Nested(SeasonSchema, many=True)














