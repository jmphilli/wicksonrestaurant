from typing import Tuple

from flask import Flask

from app import settings
from app.constants import HTTP_400_BAD_REQUEST
from app.exceptions import BadRequest
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

    @app.handle_exception(BadRequest)
    def handle_bad_request(_: BadRequest) -> Tuple[str, int]:
        return "{}", HTTP_400_BAD_REQUEST

    return app
