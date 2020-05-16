import json
from typing import Tuple

from flask import Blueprint
from flask import request

from app.constants import HTTP_200_OK
from app.constants import HTTP_400_BAD_REQUEST
from app.core_services.order import default_order_core_service

blueprint = Blueprint("inventory", __name__)


@blueprint.route("/add-line-item", methods=["POST"])
def add_line_item() -> Tuple[str, int]:
    data = request.get_data()
    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        return "{}", HTTP_400_BAD_REQUEST
    order_id = parsed_data.get("order_id")
    inventory_item_id = parsed_data.get("inventory_item_id")
    order_id = default_order_core_service().add_line_item(
        order_id=order_id, inventory_item_id=inventory_item_id,
    )

    return json.dumps({"order_id", order_id}), HTTP_200_OK
