from flask import Flask

from app import settings
from app.routes import cart
from app.routes import inventory


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)

    # register blueprints
    app.register_blueprint(cart.blueprint)
    app.register_blueprint(inventory.blueprint)

    @app.route("/healthcheck")
    def healthcheck() -> str:
        return "OK"

    return app
