from typing import Optional
from cloverapi.cloverapi_client import CloverApiClient
from app.settings import SANDBOX_URL, API_KEY, MERCHANT_ID


DEFAULT_CLOVER_API_CLIENT: Optional[CloverApiClient] = None


def default_clover_api_client() -> CloverApiClient:
    global DEFAULT_CLOVER_API_CLIENT
    if DEFAULT_CLOVER_API_CLIENT is None:
        DEFAULT_CLOVER_API_CLIENT = CloverApiClient(api_key=API_KEY, merchant_id=MERCHANT_ID, api_url=SANDBOX_URL)
    return DEFAULT_CLOVER_API_CLIENT


class CloverService:
    def __init__(self, clover_client: Optional[CloverApiClient] = None) -> None:
        self.clover_client = clover_client or default_clover_api_client()

    def get_inventory(self):
        return self.clover_client.inventory_service.get_inventory_items()

    def create_order(self):
        state = {"state": "open"}
        self.clover_client.order_service.create_order(state)

    def add_line_item(self, order_id: int, inventory_item_id: str):
        body = {'item': {'id': inventory_item_id}}
        self.clover_client.order_service.create_line_item(order_id, line_item=body)


DEFAULT_CLOVER_SERVICE: Optional[CloverService] = None


def default_clover_service() -> CloverService:
    global DEFAULT_CLOVER_SERVICE
    if DEFAULT_CLOVER_SERVICE is None:
        DEFAULT_CLOVER_SERVICE = CloverService()
    return DEFAULT_CLOVER_SERVICE
