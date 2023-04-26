from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    @app.after_request
    def add_cors(response):
        response.headers.set('Access-Control-Allow-Origin', '*')
        return response

    with app.app_context():
        from . import views

    return app 