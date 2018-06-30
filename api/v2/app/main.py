from flask import Blueprint, send_from_directory

main = Blueprint('main', __name__)

@main.route('/')
def handle_api():
    return send_from_directory('./docs', 'output.html')