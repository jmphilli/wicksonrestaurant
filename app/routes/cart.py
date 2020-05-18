import json
from typing import cast
from typing import Tuple

from flask import Blueprint

from app.constants import HTTP_200_OK
from app.core_services.order import default_order_core_service
from app.routes.helpers import get_json

blueprint = Blueprint("cart", __name__)


@blueprint.route("/add-line-item", methods=["POST"])
def add_line_item() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = parsed_data.get("order_id")
    inventory_item_id = cast(str, parsed_data.get("inventory_item_id"))
    order_id = default_order_core_service().add_line_item(
        order_id=order_id, inventory_item_id=inventory_item_id,
    )

    return json.dumps({"order_id": order_id}), HTTP_200_OK


@blueprint.route("/calculate-order-total", methods=["POST"])
def calculate_order_total() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = cast(str, parsed_data.get("order_id"))
    total = default_order_core_service().calculate_order_total(order_id)
    return json.dumps({"order_total": total}), HTTP_200_OK
