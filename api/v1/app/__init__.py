from flask import Flask, jsonify

from instance.config import app_config
  
URL_PREFIX = '/api/v1'

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    from app.auth.view import auth
    app.register_blueprint(auth, url_prefix=URL_PREFIX+'/auth/')

    return app
