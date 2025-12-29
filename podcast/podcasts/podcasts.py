from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo

import podcast.podcasts.services as services

podcasts_bp = Blueprint('podcasts_bp', __name__)


@podcasts_bp.route('/podcasts', methods=['GET'])
def show_podcasts():
    podcasts = services.get_podcasts_by_alphabet(services.get_list_of_podcasts_titles(repo.repo_instance),
                                                 repo.repo_instance)
    page = request.args.get('page', 1, type=int)

    podcasts_on_page, total = services.pagination(page, podcasts)
    return render_template('catalogue.html', podcasts_on_page=podcasts_on_page,
                           total=total, page=page)


