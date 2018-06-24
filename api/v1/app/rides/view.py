from flask import Blueprint, jsonify, request

# Local imports
from app.models import User, Rides
from app.auth.helper import token_required

rides = Blueprint('rides', __name__)

@rides.route('/rides', methods=['GET', 'POST'])
@token_required
def handle_rides(crate_user):
    if request.method == 'POST':
        payload = request.get_json()

        origin = payload['origin']
        destination = payload['destination']
        car_model = payload['car_model']
        driver_name = payload['driver_name']
        depature = payload['depature']
        ride = Rides(origin=origin, destination=destination, 
                     car_model=car_model, driver_name=driver_name,
                     depature=depature)
        ride.save()
        return jsonify({
            'message': 'create ride offer',
            'rides': ride.dicts()
        })
    else:
        return jsonify({
            'message':Rides.db_rides
        })