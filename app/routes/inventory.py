import json
from typing import Tuple

from flask import Blueprint

from app.constants import HTTP_200_OK
from app.services.clover_gateway import default_clover_service

blueprint = Blueprint("inventory", __name__)


@blueprint.route("/inventory", methods=["GET"])
def get_inventory() -> Tuple[str, int]:
    inventory = default_clover_service().get_inventory()
    response = []
    for item in inventory:
        category = None
        categories = item.get("categories", {}).get("elements", [])
        if categories:
            category = categories[0].get("name")
        response.append(
            {
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "category": category,
            },
        )

    return (
        json.dumps(response),
        HTTP_200_OK,
    )
