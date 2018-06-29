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
        c = []
        for u in row:
            work= {
            'ride id': u[0],
            'user id': u[1],
            'origin': u[2],
            'destination': u[3],
            'car model': u[4],
            'driver name': u[5],
            'depature': u[6],
            'status': 'ok'}
            c.append(work)
        return jsonify(c)

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
@rides.route('/rides/<int:ride_id>/requests', methods=['GET', 'POST'])
@token_required
def handle_join(curr_user, ride_id):
    if request.method == 'POST':
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
                    'pickup time': row[5],
                    'accepted': row[6]})
        else:
            return jsonify({
                'message': 'Ride with that id Does not exist',
                'status': 'failed'}), 404
    else:
        if current_app.config['TESTING']:
                conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        else:
            conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
        curs = conn.cursor()
        query = 'SELECT * FROM requests'
        curs.execute(query)
        row = curs.fetchall()
        c = []
        print(row)
        for u in row:
            work = {
                'request id': u[0],
                'ride id': u[2],
                'pickup Location': u[3],
                'destination': u[4],
                'pickup time': u[5],
                'accepted': u[6],
            }
            c.append(work)
        return jsonify(c)

'''
Route for accepting or rejecting ride offers
'''
@rides.route('/rides/<int:ride_id>/requests/<int:req_id>', methods=['PUT'])
@token_required
def handle_action_request(curr_user,ride_id, req_id):
    payload = request.get_json()
    action = payload['accepted']
    if action == 'True' or action == 'true':
        if current_app.config['TESTING']:
                conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        else:
            conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
        curs = conn.cursor()
        query = "UPDATE requests SET accepted = %s where request_id = %s"
        curs.execute(query, (action, req_id,))
        conn.commit()
        return jsonify({
                'message': 'request successfully accepted',
                'status': 'updated'}), 201
    else:
        return jsonify({
                    'message': 'you have not accepted request',
                    'accepted': 'False'}), 200
    