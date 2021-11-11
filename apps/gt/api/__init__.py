import datetime

from flask import Flask, request

from packages.datetime_utils import datetime_to_str
from packages.geoip import Geoip


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # a simple page that says hello
    @app.route('/hello', methods=["get"])
    def hello():
        ip = request.remote_addr
        geo_data = Geoip("gtapi").get_geo_data(ip).__dict__
        now = datetime_to_str(datetime.datetime.utcnow())
        return f'Hello, World! Time: {now}, IP: {ip}, Geo data: {geo_data}\n'

    return app


# assign the flask app to be picked up by wsgi
application = create_app()


# if not __main__, this file is called from apache and started from the wsgi extension
# So the main will never be called in prod to start the application.
if __name__ == "__main__":
    application.run()
