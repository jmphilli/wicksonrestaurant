import json
from typing import cast
from typing import Tuple

from flask import Blueprint
from flask import request

from app.constants import HTTP_200_OK
from app.constants import HTTP_400_BAD_REQUEST
from app.core_services.order import default_order_core_service
from app.routes.helpers import get_json

blueprint = Blueprint("customer", __name__)


@blueprint.route("/add-customer", methods=["POST"])
def add_customer_to_order() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = parsed_data.get("order_id")
    first_name = parsed_data.get("first_name")
    last_name = parsed_data.get("last_name")
    email = parsed_data.get("email")
    note = parsed_data.get("note")
    phone = parsed_data.get("phone")
    if not first_name or not last_name or not email or not phone:
        return json.dumps({"error": "required field missing"}), HTTP_400_BAD_REQUEST
    customer_id, order_id = default_order_core_service().add_customer_to_order(
        order_id=order_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        note=note,
    )
    return json.dumps({"customer_id": customer_id, "order_id": order_id}), HTTP_200_OK


@blueprint.route("/customer", methods=["GET"])
def get_customer_from_order() -> Tuple[str, int]:
    order_id = request.args.get("order_id")
    if not order_id:
        return "{}", HTTP_400_BAD_REQUEST
    order_id = cast(str, order_id)
    return (
        json.dumps(
            default_order_core_service().get_customer_from_order(order_id=order_id),
        ),
        HTTP_200_OK,
    )
