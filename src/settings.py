import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()


def configure_app(app):
    app.config.FLASK_ENV = os.getenv("FLASK_ENV")
    app.config.FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    app.config.FLASK_PROTOCOL = os.getenv("FLASK_PROTOCOL")
    app.config.FLASK_HOST = os.getenv("FLASK_HOST")
    app.config.FLASK_PORT = os.getenv("FLASK_PORT")

    # KILLBILL
    app.config.KB_API_URL = os.getenv("KB_API_URL")
    app.config.KB_USERNAME = os.getenv("KB_USERNAME")
    app.config.KB_PASSWORD = os.getenv("KB_PASSWORD")
    app.config.KB_TENANT = os.getenv("KB_TENANT")
    app.config.KB_API_KEY = os.getenv("KB_API_KEY")
    app.config.KB_API_SECRET = os.getenv("KB_API_SECRET")
    app.config.KB_TIMEOUT = 30

    # add more .env secrets here ...
