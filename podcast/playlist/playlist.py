from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
import podcast.adapters.repository as repo

import podcast.playlist.services as services
from podcast.authentication.authentication import login_required

from podcast.domainmodel.model import Episode

playlist_bp = Blueprint('playlist_bp', __name__)


@playlist_bp.route('/playlist', methods=['GET'])
@login_required
def show_playlist(page=0):
    username = session['user_name']
    playlist_episodes = services.get_user_playlist(username, repo.repo_instance)
    ep_list = playlist_episodes.list_of_episodes

    playlist_page = request.args.get('page', 1, type=int)

    # This counts how many times next, previous, and, etc. have been pressed
    counter = request.args.get('counter', -1, type=int)

    episodes_on_page, total = services.pagination(playlist_page, ep_list)

    ep_pod_dict = services.episode_podcast_dict(episodes_on_page, repo.repo_instance)
    return render_template('playlist.html',
                           ep_list=episodes_on_page,
                           name=username,
                           page=playlist_page,
                           total=total,
                           counter=counter,
                           ep_pod_dict=ep_pod_dict)


@playlist_bp.route('/remove_episode/<int:episode_id>')
@login_required
def remove_episode(episode_id, counter=0, page=0):
    username = session['user_name']

    counter = request.args.get('counter', -1, type=int)
    page = request.args.get('page', 1, type=int)

    playlist = services.get_user_playlist(username, repo.repo_instance)
    episode = services.get_episode_by_id(episode_id, repo.repo_instance)
    services.remove_episode_from_playlist(playlist, episode, repo.repo_instance)
    flash("Episode removed")

    return redirect(url_for('playlist_bp.show_playlist', page=page))
