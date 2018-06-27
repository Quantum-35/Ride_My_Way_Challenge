from flask import Blueprint

from app.auth.helpers import token_required

rides = Blueprint('rides', __name__)

@rides.route('/rides')
@token_required
def handle_ride(current_app):
    return 'Hello world'