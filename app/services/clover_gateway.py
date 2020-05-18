from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from cloverapi.cloverapi_client import CloverApiClient

from app.settings import API_KEY
from app.settings import MERCHANT_ID
from app.settings import SANDBOX_URL


DEFAULT_CLOVER_API_CLIENT: Optional[CloverApiClient] = None


def default_clover_api_client() -> CloverApiClient:
    global DEFAULT_CLOVER_API_CLIENT
    if DEFAULT_CLOVER_API_CLIENT is None:
        DEFAULT_CLOVER_API_CLIENT = CloverApiClient(
            api_key=API_KEY, merchant_id=MERCHANT_ID, api_url=SANDBOX_URL,
        )
    return DEFAULT_CLOVER_API_CLIENT


class CloverService:
    def __init__(self, clover_client: Optional[CloverApiClient] = None) -> None:
        self.clover_client = clover_client or default_clover_api_client()

    def get_inventory(self) -> List[Dict[str, Any]]:
        raw_data = self.clover_client.inventory_service.get_inventory_items()
        return raw_data.get("elements", {})

    def create_order(self) -> str:
        state = {"state": "open"}
        resp = self.clover_client.order_service.create_order(state)
        return resp.get("id")

    def add_line_item(self, order_id: str, inventory_item_id: str) -> None:
        body = {"item": {"id": inventory_item_id}}
        self.clover_client.order_service.create_line_item(
            order_id, line_item=body,
        )

    def get_line_items_for_order(self, order_id: str) -> List[Dict[str, Any]]:
        data = self.clover_client.order_service.get_line_items_by_order(
            order_id=order_id,
        )
        line_items = data["elements"]
        return line_items

    def get_pay_info(self) -> None:
        # possibly unused?
        return self.clover_client.merchant_service.get_gateway()


DEFAULT_CLOVER_SERVICE: Optional[CloverService] = None


def default_clover_service() -> CloverService:
    global DEFAULT_CLOVER_SERVICE
    if DEFAULT_CLOVER_SERVICE is None:
        DEFAULT_CLOVER_SERVICE = CloverService()
    return DEFAULT_CLOVER_SERVICE
