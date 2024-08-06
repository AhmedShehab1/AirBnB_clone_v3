#!/usr/bin/python3
"""
Defines actaul instance of Flask
frameworks
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(error):
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True)
