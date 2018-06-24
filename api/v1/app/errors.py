from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def route_not_found(e):
    """
    Return a custom 404 Http response message for missing or not found routes.
    
    """
    return jsonify({
        'message': 'Endpoint not found',
        'status': 'Failed'}), 404


@errors.app_errorhandler(405)
def method_not_found(e):
    """
    Custom response for methods not allowed for the requested URLs
    
    """
    return jsonify({
        'message': 'The method is not allowed for the requested URL',
        'status': 'Failed'}), 405


@errors.app_errorhandler(500)
def internal_server_error(e):
    """
    Return a custom message for a 500 internal error
    """
    return jsonify({
        'message': 'Internal server error',
        'status': 'Failed'}), 500
