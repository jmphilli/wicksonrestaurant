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
        raw_data = self.clover_client.inventory_service.get_inventory_items(
            expand="categories",
        )
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

    def remove_line_item(self, order_id: str, line_item_id: str) -> None:
        body = {"lineItem": {"id": line_item_id}}
        self.clover_client.order_service.void_line_item(
            order_id=order_id, voided_line_item=body,
        )

    def add_tip(
        self, order_id: str, tip_amount: int, existing_line_item_id: Optional[str],
    ) -> None:
        body = {
            "price": tip_amount,
            "name": "tip",
        }
        if existing_line_item_id:
            # update_line_item_by_id doesn't work on clover's side
            self.clover_client.order_service.void_line_item_by_id(
                order_id=order_id, line_item_id=existing_line_item_id,
            )
        self.clover_client.order_service.create_line_item(order_id, line_item=body)

    def get_line_items_for_order(self, order_id: str) -> List[Dict[str, Any]]:
        data = self.clover_client.order_service.get_line_items_by_order(
            order_id=order_id,
        )
        line_items = data["elements"]
        return line_items

    def pay_for_order(self, order_id: str, stripe_reference: str, total: int) -> None:
        payload = {
            "id": order_id,
            "externalReferenceId": stripe_reference,
            "paymentState": "PAID",
            "state": "locked",
            "total": total,
        }
        self.clover_client.order_service.update_order_by_id(payload)

    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self.clover_client.order_service.get_order_by_id(order_id=order_id)

    def add_note_to_order(self, order_id: str, note: str) -> None:
        payload = {
            "id": order_id,
            "note": note,
        }
        self.clover_client.order_service.update_order_by_id(payload)

    def create_customer(
        self, first_name: str, last_name: str, email: str, phone: str,
    ) -> str:
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "emailAddresses": [{"emailAddress": email}],
            "phoneNumbers": [{"phoneNumber": phone}],
        }
        resp = self.clover_client.customer_service.create_customer(payload)
        return resp["id"]

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self.clover_client.customer_service.get_customer_by_id(
            customer_id, include_emails=True, include_phones=True,
        )

    def add_customer_to_order(self, order_id: str, customer_id: str) -> None:
        payload = {"id": order_id, "customers": [{"id": customer_id}]}
        self.clover_client.order_service.update_order_by_id(payload)


DEFAULT_CLOVER_SERVICE: Optional[CloverService] = None


def default_clover_service() -> CloverService:
    global DEFAULT_CLOVER_SERVICE
    if DEFAULT_CLOVER_SERVICE is None:
        DEFAULT_CLOVER_SERVICE = CloverService()
    return DEFAULT_CLOVER_SERVICE
