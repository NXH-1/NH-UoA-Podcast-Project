import os

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import podcast.adapters.repository as repo

import podcast.description.services as services
from podcast.authentication.authentication import login_required

description_bp = Blueprint('description_bp', __name__)


@description_bp.route('/description/<int:podcast_id>', methods=['GET', 'POST'])
def show_description(podcast_id, counter=0, page=0):
    podcast = services.get_podcast_by_id(podcast_id, repo.repo_instance)
    podcast_episodes = services.get_episodes(podcast_id, repo.repo_instance)
    podcast_episodes = services.episodes_to_dict(podcast_episodes)

    episode_page = request.args.get('page', 1, type=int)

    # This counts how many times next, previous, and, etc. have been pressed
    counter = request.args.get('counter', -1, type=int)

    episodes_on_page, total = services.pagination(episode_page, podcast_episodes)

    logged_in = True

    playlist = []
    if session.get('user_name') is not None:
        username = session['user_name']
        playlist = services.get_user_playlists(username, repo.repo_instance).list_of_episodes
        playlist = services.episodes_to_dict(playlist)
    else:
        logged_in = False

    # Reviews stuff
    average_rating = services.get_average_podcast_rating(podcast_id, repo.repo_instance)
    podcast_to_show_reviews = len(podcast['reviews'])

    return render_template('podcastDescription.html',
                           podcast=podcast,
                           episodes=episodes_on_page,
                           total=total,
                           page=episode_page,
                           counter=counter,
                           playlist=playlist,
                           logged_in=logged_in,
                           podcast_id=podcast_id,
                           podcast_to_show_reviews=podcast_to_show_reviews,
                           average_rating=average_rating)


@description_bp.route('/add_to_playlist/<int:episode_id>', methods=['GET', 'POST'])
@login_required
def add_to_playlist(episode_id, counter=0, page=0):
    username = session['user_name']

    counter = request.args.get('counter', -1, type=int)
    page = request.args.get('page', 1, type=int)

    playlist = services.get_user_playlists(username, repo.repo_instance)
    episode = services.get_episode_by_id(episode_id, repo.repo_instance)
    services.add_episode_to_playlist(playlist, episode, repo.repo_instance)
    flash("Episode added", 'add')
    return redirect(url_for('description_bp.show_description', podcast_id=episode.pod_id, counter=counter, page=page))


@description_bp.route('/remove_from_playlist/<int:episode_id>')
@login_required
def remove_from_playlist(episode_id, counter=0, page=0):
    username = session['user_name']

    counter = request.args.get('counter', -1, type=int)
    page = request.args.get('page', 1, type=int)

    playlist = services.get_user_playlists(username, repo.repo_instance)
    episode = services.get_episode_by_id(episode_id, repo.repo_instance)
    services.remove_episode_from_playlist(playlist, episode, repo.repo_instance)
    flash("Episode removed", 'remove')
    return redirect(url_for('description_bp.show_description', podcast_id=episode.pod_id, counter=counter, page=page))


@description_bp.route('/add_podcast_to_playlist/<int:podcast_id>', methods=['GET', 'POST'])
@login_required
def add_podcast_to_playlist(podcast_id, counter=0, page=0):
    username = session['user_name']

    counter = request.args.get('counter', -1, type=int)
    page = request.args.get('page', 1, type=int)

    playlist = services.get_user_playlists(username, repo.repo_instance)

    temp = []
    for episode in playlist.list_of_episodes:
        temp.append(episode)

    services.add_all_episodes_to_playlist(playlist, podcast_id, repo.repo_instance)

    if playlist.list_of_episodes != temp:
        flash("All episodes in Podcast ADDED", 'add')
    return redirect(url_for('description_bp.show_description', podcast_id=podcast_id, counter=counter, page=page))


@description_bp.route('/remove_podcast_from_playlist/<int:podcast_id>', methods=['GET', 'POST'])
@login_required
def remove_podcast_from_playlist(podcast_id, counter=0, page=0):
    username = session['user_name']

    counter = request.args.get('counter', -1, type=int)
    page = request.args.get('page', 1, type=int)

    playlist = services.get_user_playlists(username, repo.repo_instance)

    temp = []
    for episode in playlist.list_of_episodes:
        temp.append(episode)

    services.remove_all_episodes_from_playlist(playlist, podcast_id, repo.repo_instance)

    if playlist.list_of_episodes != temp:
        flash("All episodes in Podcast REMOVED", 'remove')
    return redirect(url_for('description_bp.show_description', podcast_id=podcast_id, counter=counter, page=page))



@description_bp.route('/add_review/<int:podcast_id>', methods=['GET', 'POST'])
@login_required
def review_on_podcast(podcast_id):
    username = session['user_name']

    counter = request.args.get('counter', -1, type=int)

    podcast = services.get_podcast_by_id(podcast_id, repo.repo_instance)
    form = ReviewForm()
    if form.validate_on_submit():

        services.add_review_to_podcast(username, podcast_id, form.comment.data, int(form.rating.data), repo.repo_instance)
        flash("commented", 'commented')
        return redirect(url_for('description_bp.show_description', podcast_id=podcast_id, counter=counter, page=0))

    return render_template('review_and_rating_of_podcast.html',
                           podcast_id=podcast_id,
                           podcast=podcast,
                           form=form,
                           handler_url=url_for('description_bp.show_description', podcast_id=podcast_id),
                           )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    podcast_id = HiddenField("Article id")
    rating = SelectField('Rating', choices=[(str(i), str(i)) for i in range(0, 6)], validators=[DataRequired()])
    submit = SubmitField('Submit')
