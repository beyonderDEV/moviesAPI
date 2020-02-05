from flask import Blueprint, jsonify, request, flash, redirect, render_template, redirect, url_for
from . import db
from .models import Movie
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('welcome.html')


@main.route('/add_movie', methods=['POST', 'GET'])
def add_movie_post():
    if request.method == 'POST':
        title = request.form.get('movie_title')
        rating = int(request.form.get('rating'))
        description = request.form.get('desc')
        movie_new = Movie(title=title, rating=rating, description=description)
        db.session.add(movie_new)
        db.session.commit()
        return redirect(url_for('main.movies')), 201
    return render_template('add_movie.html')


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
        movies.append({'title': movie.title, 'rating': movie.rating, 'desc:' : movie.description})
    return jsonify({'movies': movies})


@main.route('/movies/<int:id>')
def description(id):
    movie_data = Movie.query.all()
    for movie in movie_data:
        if movie.id == id:
            result = {'desc: ': movie.description}
    return jsonify({'movie': result})