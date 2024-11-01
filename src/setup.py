from flask import Flask  # type: ignore
from src.logger import Logger
from src.settings import configure_app, configure_services


def create_app():
    app = Flask(__name__)

    configure_app(app)
    configure_services(app)

    from .routes import config, listener

    app.register_blueprint(config.bp)
    app.register_blueprint(listener.bp)
    # add more custom routes here ...

    return app
