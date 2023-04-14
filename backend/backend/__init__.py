from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    with app.app_context():
        from . import views

    return app 