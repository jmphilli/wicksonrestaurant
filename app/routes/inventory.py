import json
from typing import Tuple

from flask import Blueprint

from app.constants import HTTP_200_OK
from app.services.clover_gateway import default_clover_api_client

blueprint = Blueprint("inventory", __name__)


@blueprint.route("/inventory", methods=["GET"])
def get_inventory() -> Tuple[str, int]:
    inventory = default_clover_api_client().inventory_service.get_inventory_items()[
        "elements"
    ]

    return (
        json.dumps(inventory),
        HTTP_200_OK,
    )
