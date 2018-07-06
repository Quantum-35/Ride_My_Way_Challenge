import psycopg2
from flask import current_app

from app.app import create_app

'''
This module creates tables for all the users and rides
'''

def create_tables():
    # Connection to the database
    if current_app.config['TESTING']:
        conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")    
    else :
        conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                        database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()
    tbl_users = (
        """
        CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(30) NOT NULL,
                email VARCHAR(30) NOT NULL,
                address VARCHAR(20),
                password VARCHAR(100) NOT NULL)
        """)
    curs.execute(tbl_users)

    conn.commit()
    return 'Success'

def create_rides():
    # Connection to the database
    if current_app.config['TESTING']:
        conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
            
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()

    tbl_rides = (
        """
         CREATE TABLE IF NOT EXISTS ride (
                ride_id SERIAL PRIMARY KEY,
                user_id INTEGER 
                REFERENCES users (id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                origin VARCHAR(30),
                destination VARCHAR(30),
                car_model VARCHAR(50),
                driver_name VARCHAR(50),
                seats VARCHAR(100),
                depature VARCHAR(30))
        """)
    curs.execute(tbl_rides)

    conn.commit()
    return 'Success'

def create_requests():
    # Connection to the database
    if current_app.config['TESTING']:
        conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
            
    else :
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
    curs = conn.cursor()

    tbl_requests = (
        """
         CREATE TABLE IF NOT EXISTS requests (
                request_id SERIAL PRIMARY KEY,
                user_id INTEGER 
                REFERENCES users (id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                ride_id INTEGER 
                REFERENCES ride (ride_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                pickup VARCHAR(30),
                destination VARCHAR(50),
                pickuptime VARCHAR(50),
                accepted VARCHAR(5))
        """)
    curs.execute(tbl_requests)

    conn.commit()
    return 'Success'