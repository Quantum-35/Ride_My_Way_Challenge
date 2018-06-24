from flask import Blueprint, jsonify, request

# Local imports
from app.models import User, Rides
from app.auth.helper import token_required

rides = Blueprint('rides', __name__)

@rides.route('/rides/', methods=['GET', 'POST'])
@token_required
def handle_rides(curr_user):
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
        return jsonify( ride.dicts()), 201
    else:
        return jsonify({
            'message':Rides.db_rides,
            'status': 'ok'
        }), 200

@rides.route('/rides/<int:ride_id>', methods=['GET'])
@token_required
def handle_singleroute(curr_user, ride_id):
    selected_ride = Rides.db_rides
    if selected_ride:
        ride = [x for x in selected_ride if x['id'] == ride_id]
        if ride:
            return jsonify({
            'message': ride,
            'status': 'ok'}), 200
        else:
            return jsonify({
            'message': 'Ride with that id Does not exist',
            'status': 'Failed'}), 404
    else:
        return jsonify({
        'message': 'Ride with that id Does not exist',
        'status': 'Failed'
    }), 404
    