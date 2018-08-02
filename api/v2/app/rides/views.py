import psycopg2
from flask import Blueprint, request, jsonify, current_app

from app.auth.helpers import token_required

from app.models import Rides, Requests

rides = Blueprint('rides', __name__)

@rides.route('/rides', methods=['GET'])
@token_required
def handle_rides(email):
    if current_app.config['TESTING']:
        conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
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
        'Number of seats': u[6],
        'depature': u[7],
        'status': 'ok'}
        c.append(work)
    return jsonify(c)

'''
Route for user Posting new ride
'''
@rides.route('/users/rides', methods=['POST'])
@token_required
def handle_created_ride(current_user):
        payload = request.get_json()
        origin = payload['origin']
        destination = payload['destination']
        car_model = payload['car_model']
        driver_name = payload['driver_name']
        seats = payload['seats']
        depature = payload['depature']
        if origin == '' or destination == '' or car_model == '' or driver_name == '' or depature == '' or seats =='':
            return jsonify({
                    'message': 'You cannot send empty fields',
                    'status': 'failed'}), 400
        ride = Rides(user_id=current_user[0],origin=origin, destination=destination,
                        car_model=car_model, driver_name=driver_name,
                        depature=depature , seats=seats)
        ride.save_ride()
        return jsonify({'message': 'Ride Successfully Created',
                        'status': 'ok'}), 201

'''
Route wher users can access details of  single ride from the available ones
'''
@rides.route('/rides/<int:ride_id>', methods=['GET'])
@token_required
def handle_singleroute(current_user, ride_id):
    if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else:
         conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
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
            'seats': row[6],
            'depature': row[7],
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
    print('current user form decorator',curr_user[0])
    if pickup=='' or destination =='' or pickuptime == '':
        return jsonify({
            'message': 'You cant make an empty ride',
            'status': 'failed'}), 400
    if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()
    query = 'SELECT * FROM ride WHERE ride_id=%s'
    curs.execute(query, (ride_id,))
    row = curs.fetchone()
    query = 'SELECT * FROM ride WHERE ride_id=%s'
    curs.execute(query, (ride_id,))
    row = curs.fetchone()
    if row[1] != curr_user[0]:
        if row:
            ride_request = Requests(row[1], row[0], curr_user[0],pickup, destination, pickuptime)
            ride_request.save_request()
            query = 'SELECT * FROM requests WHERE ride_id=%s'
            curs.execute(query, (ride_id,))
            row = curs.fetchone()
            print(row)
            return jsonify({
                    'request id':row[0],
                    'created By': row[1],
                    'ride_id': row[2],
                    'joined by': row[3],
                    'pickup': row[4],
                    'destination': row[5],
                    'pickup time': row[6],
                    'accepted': row[7]})
        else:
            return jsonify({
                'message': 'Ride with that id Does not exist',
                'status': 'failed'}), 404
    else:
        return jsonify({
                'message': 'You can not make request to ride that you created',
                'status': 'failed'}), 400
''''
Route for user fetching all the ride requests
'''
@rides.route('/users/rides/<int:ride_id>/requests', methods=['GET'])
@token_required
def handle_fetch_ride_requests(curr_user, ride_id):
    if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()
    query = 'SELECT * FROM requests WHERE ride_id=%s'
    curs.execute(query, (ride_id,))
    row = curs.fetchall()
    if row:
        c = []
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
    else:
        return jsonify({
            'message': 'sorry, ride with that id does not exist',
            'status': 'failed'}), 404

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
        else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
        curs = conn.cursor()
        query = 'SELECT * FROM requests WHERE ride_id=%s'
        curs.execute(query, (ride_id,))
        row = curs.fetchall()
        if row:
            query = "UPDATE requests SET accepted = %s where request_id = %s"
            curs.execute(query, (action, req_id,))
            conn.commit()
            query = "SELECT * FROM ride WHERE ride_id=%s"
            curs.execute(query,(ride_id,))
            row3 = curs.fetchone()
            seat = int(row3[6]) - int(1)
            query = "UPDATE ride SET seats = %s  WHERE ride_id=%s"
            curs.execute(query,(seat, ride_id,))
            conn.commit()
            return jsonify({
                    'message': 'request successfully accepted',
                    'status': 'ok'}), 201
        else:
            return jsonify({
                    'message': 'Sorry, car with that id does not exist',
                    'status': 'failed'}), 404
    elif action=='False' or action=='false':
        if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
        curs = conn.cursor()
        query = 'SELECT * FROM requests WHERE ride_id=%s'
        curs.execute(query, (ride_id,))
        row = curs.fetchall()
        if row:
            query = "UPDATE requests SET accepted = %s where request_id = %s"
            curs.execute(query, (action, req_id,))
            conn.commit()
            return jsonify({
                    'message': 'request successfully rejected',
                    'status': 'ok'}), 201
    else:
        return jsonify({
                    'message': 'you have not accepted request',
                    'accepted': 'False'}), 200

    
@rides.route('/requests', methods=['GET'])
@token_required
def handle_get_action_request(curr_user):
    if current_app.config['TESTING']:
        conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()
    query = 'SELECT * FROM requests WHERE user_id = %s'
    curs.execute(query, (curr_user[0],))
    row = curs.fetchall()
    if row:
        c = []
        for u in row:
            work= {
            'request id': u[0],
            'user id': u[1],
            'ride id': u[2],
            'pickup': u[3],
            'destination': u[4],
            'pickuptime': u[5],
            'accepted': u[6],
            'status': 'ok'}
            c.append(work)
        return jsonify(c)
    else:
        return jsonify({
            'message': 'You have no Requests ',
            'status': 'failed'}), 404

    # Custom endpoints 
@rides.route('/user/myrides', methods=['GET'])
@token_required
def handle_get_all_rides_user_has_taken(curr_user):
    if current_app.config['TESTING']:
        conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()
    print(curr_user)
    query = 'SELECT * FROM requests WHERE user_requested_id = %s'
    curs.execute(query, (curr_user[0],))
    row = curs.fetchall()
    if row:
        c = []
        for u in row:
            work= {
            'request id': u[0],
            'created by': u[1],
            'ride id': u[2],
            'joined by': u[3],
            'pickup': u[4],
            'destination': u[5],
            'pickuptime': u[6],
            'accepted': u[7],
            'status': 'ok'}
            c.append(work)
        return jsonify(c)
    else:
        return jsonify({
            'message':'You have never Joined any Ride request',
            'status': 'failed'}), 404

# # User Can Delete Ride reques
# @rides.route('/user/rides/<int:ride_id>/requests', methods=['DELETE'])
# @token_required
# def handle_delete_ride(curr_user):
#     if current_app.config['TESTING']:
#         conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
#     else :
#             conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
#                                 database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
#     curs = conn.cursor()
#     print(curr_user)
#     query = 'SELECT * FROM requests WHERE user_requested_id = %s'
#     curs.execute(query, (curr_user[0],))
#     row = curs.fetchall()