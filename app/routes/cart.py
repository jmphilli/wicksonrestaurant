import json
import smtplib
from typing import cast
from typing import Tuple

import stripe
from flask import Blueprint
from flask import request

from app.constants import HTTP_200_OK
from app.constants import HTTP_400_BAD_REQUEST
from app.constants import HTTP_500_INTERNAL_SERVER_ERROR
from app.core_services.order import default_order_core_service
from app.exceptions import BadRequest
from app.routes.helpers import get_json
from app.settings import STRIPE_SECRET_KEY

blueprint = Blueprint("cart", __name__)

# needed to properly configure the stripe integration
stripe.api_key = STRIPE_SECRET_KEY


@blueprint.route("/add-line-item", methods=["POST"])
def add_line_item() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = parsed_data.get("order_id")
    inventory_item_id = cast(str, parsed_data.get("inventory_item_id"))
    order_id = default_order_core_service().add_line_item(
        order_id=order_id, inventory_item_id=inventory_item_id,
    )

    return json.dumps({"order_id": order_id}), HTTP_200_OK


@blueprint.route("/remove-line-item", methods=["POST"])
def remove_line_item() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = parsed_data.get("order_id")
    inventory_item_id = cast(str, parsed_data.get("inventory_item_id"))
    order_id = default_order_core_service().remove_line_item(
        order_id=order_id, inventory_item_id=inventory_item_id,
    )

    return json.dumps({"order_id": order_id}), HTTP_200_OK


@blueprint.route("/add-tip", methods=["POST"])
def add_tip() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = cast(str, parsed_data.get("order_id"))
    tip_amount = cast(int, parsed_data.get("tip_amount"))

    # todo remove existing tip line item if exists
    default_order_core_service().add_tip(
        order_id=order_id, tip_amount=tip_amount,
    )

    return json.dumps({"order_id": order_id}), HTTP_200_OK


@blueprint.route("/calculate-order-total", methods=["POST"])
def calculate_order_total() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = cast(str, parsed_data.get("order_id"))
    total = default_order_core_service().calculate_order_total(order_id)
    return json.dumps({"order_total": total}), HTTP_200_OK


@blueprint.route("/order-details", methods=["GET"])
def get_order_details() -> Tuple[str, int]:
    order_id = request.args.get("order_id")
    if not order_id:
        raise BadRequest
    details = default_order_core_service().get_order_details(order_id)
    return json.dumps(details), HTTP_200_OK


@blueprint.route("/charge", methods=["POST"])
def charge_order() -> Tuple[str, int]:
    parsed_data = get_json()
    order_id = cast(str, parsed_data.get("order_id"))
    payment_method_id = cast(str, parsed_data.get("payment_method_id"))
    if not order_id or not payment_method_id:
        return json.dumps({"error": "order | payment missing"}), HTTP_400_BAD_REQUEST
    total = default_order_core_service().calculate_order_total(order_id)
    if default_order_core_service().order_is_paid(order_id):
        default_order_core_service().send_email(order_id=order_id)
        return json.dumps({"success": True, "order_id": order_id}), HTTP_200_OK
    try:
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency="usd",
            payment_method=payment_method_id,
            # A PaymentIntent can be confirmed some time after creation,
            # but here we want to confirm (collect payment) immediately.
            confirm=True,
            # If the payment requires any follow-up actions from the
            # customer, like two-factor authentication, Stripe will error
            # and you will need to prompt them for a new payment method.
            error_on_requires_action=True,
        )
        if intent.status == "succeeded":
            # Handle post-payment fulfillment
            default_order_core_service().mark_order_as_paid(
                order_id=order_id, stripe_reference=intent.id, total=total,
            )
            default_order_core_service().send_email(order_id=order_id)
            return json.dumps({"success": True, "order_id": order_id}), HTTP_200_OK
        # Any other status would be unexpected, so error
        return (
            json.dumps({"error": "Invalid PaymentIntent status"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except stripe.error.CardError as e:
        # Display error on client
        return json.dumps({"error": e.user_message}), HTTP_200_OK
    except smtplib.SMTPSenderRefused as e:
        return (
            json.dumps({"error": "please try again", "message": e.smtp_error}),
            HTTP_200_OK,
        )
