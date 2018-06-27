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
            
    else:
        conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
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
