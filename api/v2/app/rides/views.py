from flask import Blueprint, request, jsonify

from app.auth.helpers import token_required

from app.models import Rides

rides = Blueprint('rides', __name__)

@rides.route('/rides', methods=['GET', 'POST'])
@token_required
def handle_rides(current_user):
    if request.method == 'POST':
        payload = request.get_json()
        origin = payload['origin']
        destination = payload['destination']
        car_model = payload['car_model']
        driver_name = payload['driver_name']
        depature = payload['depature']
        ride = Rides(user_id=current_user[0],origin=origin, destination=destination,
                        car_model=car_model, driver_name=driver_name,
                        depature=depature)
        ride.save_ride()
        return jsonify({'message': 'Ride Successfully Created',
                        'status': 'ok'}), 201
    else:
        return jsonify({
            'message': 'Rides.db_rides',
            'status': 'ok'
        }), 200