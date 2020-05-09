from flask import Blueprint
from app.services.clover_gateway import default_clover_api_client
from app.constants import HTTP_200_OK

blueprint = Blueprint("inventory", __name__)


@blueprint.route("/inventory", methods=["GET"])
def get_inventory():
    return default_clover_api_client().inventory_service.get_inventory_items(), HTTP_200_OK
