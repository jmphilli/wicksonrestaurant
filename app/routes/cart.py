import json

from flask import Blueprint
from flask import request

from app.constants import HTTP_200_OK
from app.constants import HTTP_400_BAD_REQUEST
from app.services.clover_gateway import default_clover_service

blueprint = Blueprint("inventory", __name__)


@blueprint.route("/add-line-item", methods=["POST"])
def add_line_item():
    data = request.get_data()
    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        return {}, HTTP_400_BAD_REQUEST
    order_id = parsed_data.get("order_id")
    if not order_id:
        # create order
        order_id = default_clover_service().create_order()
    inventory_item = parsed_data.get("inventory_item_id")
    default_clover_service().add_line_item(
        order_id=order_id, line_item=inventory_item,
    )

    return {}, HTTP_200_OK
