import psycopg2
from flask import Blueprint, request, jsonify, current_app

from app.auth.helpers import token_required

from app.models import Rides, Requests

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
        if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        else:
            conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
        curs = conn.cursor()
        query = 'SELECT * FROM ride'
        curs.execute(query)
        row = curs.fetchall()
        return jsonify({
            'result': row,
            'status': 'ok'
        }), 200

'''
Route wher users can access details of  single ride from the available ones
'''
@rides.route('/rides/<int:ride_id>', methods=['GET'])
@token_required
def handle_singleroute(current_user, ride_id):
    if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else:
        conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
    curs = conn.cursor()
    query = 'SELECT * FROM ride WHERE ride_id=%s'
    curs.execute(query, (ride_id,))
    row = curs.fetchone()
    if row:
        return jsonify({
            'ride_id': row[0],
            'origin': row[2],
            'destination': row[3],
            'car_model': row[4],
            'driver name': row[5],
            'depature': row[6],
            'status': 'ok'}), 200
    else:
        return jsonify({
            'message': 'Ride with that id Does not exist',
            'status': 'Failed'}), 404


'''
Route for users making request to existing rides
'''
@rides.route('/rides/<int:ride_id>/requests', methods=['POST'])
@token_required
def handle_join(curr_user, ride_id):
    payload = request.get_json()
    pickup = payload['pickup']
    destination = payload['destination']
    pickuptime = payload['pickuptime']

    if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else:
        conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
    curs = conn.cursor()
    query = 'SELECT * FROM ride WHERE ride_id=%s'
    curs.execute(query, (ride_id,))
    row = curs.fetchone()
    if row:
        ride_request = Requests(row[1], row[0], pickup, destination, pickuptime)
        ride_request.save_request()
        query = 'SELECT * FROM requests WHERE ride_id=%s'
        curs.execute(query, (ride_id,))
        row = curs.fetchone()
        return jsonify({
                'request id':row[0],
                'ride_id': row[2],
                'pickup': row[3],
                'destination': row[4],
                'pickup time': row[5]})
    else:
        return jsonify({
            'message': 'Ride with that id Does not exist',
            'status': 'failed'}), 404