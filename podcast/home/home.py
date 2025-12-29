from flask import Blueprint, render_template
import podcast.adapters.repository as repo
import podcast.home.services as services

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    random_podcasts = services.get_random_podcasts(repo.repo_instance)

    return render_template('/home.html', podcasts=random_podcasts)
