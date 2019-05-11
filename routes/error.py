from flask import (
    Blueprint,
    render_template,
)

main = Blueprint('error', __name__)


@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(401)
def authorized_error(error):
    return render_template('errors/401.html'), 401