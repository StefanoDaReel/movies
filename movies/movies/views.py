from flask import render_template, request, flash, redirect, url_for
from flask.views import MethodView, View

from flask_login import login_required, current_user

from movies import db
from movies.utilities import add_obj_to_db

from .models import Movie, Opinion
from .forms import MovieForm


class MovieListView(View):
    decorators = [login_required]

    def dispatch_request(self):
        movies = Movie.query.filter_by(added_by=current_user.id)
        return render_template('movies/index.html', movies=movies)


class MovieCreateView(MethodView):
    decorators = [login_required]

    def get(self):
        form = MovieForm()
        return render_template('movies/create.html', form=form)

    def post(self):
        form = MovieForm()

        if form.validate_on_submit():
            title = request.form['title']
            opinion = request.form['opinion']

            movie = Movie(
                title=title,
                added_by=current_user.id
            )

            error = add_obj_to_db(db, movie)

            if not error:
                movie_id = movie.id

                opinion = Opinion(
                    content=opinion,
                    movie_id=movie_id
                )

                error = add_obj_to_db(db, opinion)

                if not error:
                    success_message = "Dodano film."
                    flash(success_message)

                    return redirect(url_for("movies.detail", id=movie_id))

            flash(error.message)

        return render_template('movies/create.html', form=form)


class MovieDetailView(View):
    decorators = [login_required]

    def dispatch_request(self, id):
        context = {
            'movie': Movie.query.get(id),
            'opinion': Opinion.query.filter_by(movie_id=id).first(),
        }
        return render_template('movies/detail.html', **context)
