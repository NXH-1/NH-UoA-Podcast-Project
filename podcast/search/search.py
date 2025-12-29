from flask import Blueprint, render_template, request

import podcast.search.services as services
import podcast.adapters.repository as repo

search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/search', methods=["POST", "GET"])
def search():
    page = request.args.get('page', 1, type=int)
    if request.method == "POST":
        query = request.form.get('searched')
        filter_by = request.form.get('filter')
    else:
        query = request.args.get('query')
        filter_by = request.args.get('filter_by')

    results = services.search_results(repo.repo_instance, query, filter_by)

    podcasts_on_page, total = services.pagination(page, results)

    return render_template('search.html', query=query, results=podcasts_on_page,
                           total=total, page=page, filter_by=filter_by)
