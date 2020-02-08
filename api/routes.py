from flask import Blueprint, jsonify, request, redirect, render_template, \
                url_for
from . import db
from .models import Movie, Show, ShowSchema, Episode, EpisodeSchema

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('welcome.html')


@main.route('/add_movie')
def add_movie():
    return render_template('add_movie.html')


@main.route('/add_movie', methods=['POST'])
def add_movie_post():
    title = request.form.get('movie_title')
    rating = int(request.form.get('rating'))
    description = request.form.get('desc')
    movie_new = Movie(title=title, rating=rating, description=description)
    db.session.add(movie_new)
    db.session.commit()
    return redirect(url_for('main.movies'))


@main.route('/remove_movie/')
def remove_movie():
    return render_template('delete.html')


@main.route('/remove_movie/', methods=["POST"])
def remove_movie_post():
    id = request.form.get('movie_id')
    movie = db.session.query(Movie).filter(Movie.id == id).first()
    if movie:
        db.session.execute('delete from movie where id=' + str(id))
        db.session.commit()
        print('Movie has been successfully removed!')
    else:
        print('There is no movie with that id')
    return redirect(url_for('main.movies'))


@main.route('/movies')
def movies():
    movie_list = Movie.query.all()
    movies = []
    for movie in movie_list:
        movies.append({'title': movie.title, 'rating': movie.rating, 
                       'desc:': movie.description})
    return jsonify({'movies': movies})


@main.route('/movies/<int:id>')
def description(id):
    movie_data = Movie.query.all()
    for movie in movie_data:
        if movie.id == id:
            result = {'desc: ': movie.description}
    return jsonify({'movie': result})


@main.route('/update')
def update_movie():
    return render_template("update_movie.html")


@main.route('/update', methods=["POST"])
def update_movie_post():
    id = request.form.get('id')
    movie = Movie.query.filter(Movie.id == id).first()
    if movie:
        new_title = request.form.get('movie_title')
        new_rating = request.form.get('rating')
        new_desc = request.form.get("desc")
        if new_title:
            movie.title = new_title
        if new_rating:
            movie.rating = int(new_rating)
        if new_desc:
            movie.description = new_desc
        db.session.commit()
        print("Updated successfully!")
    else:
        print("There is no movie with such id!")
    return redirect(url_for("main.movies"))


@main.route('/search')
def search():
    return render_template('search.html')


@main.route('/search', methods=['POST'])
def search_post():
    q = request.form.get('q')
    if q is not None:
        res = Movie.query.whoosh_search(q).all()
        if res is not None:
            movies = []
            for movie in res:
                movies.append({'title': movie.title, 'rating': movie.rating, 
                               'desc': movie.description})
            return jsonify({'result': movies})
    return render_template('search.html')


@main.route('/shows')
def shows():
    show = Show.query.all()
    show_schema = ShowSchema(many=True)
    res = show_schema.dump(show)
    return jsonify({'shows': res})
