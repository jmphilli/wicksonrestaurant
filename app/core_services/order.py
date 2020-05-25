from typing import Optional
from typing import Tuple

from app.services.clover_gateway import CloverService
from app.services.clover_gateway import default_clover_service


class OrderCoreService:
    def __init__(self, clover_service: Optional[CloverService] = None) -> None:
        self.clover_service = clover_service or default_clover_service()

    def _ensure_order_id(self, order_id: Optional[str]) -> str:
        if not order_id:
            return self.clover_service.create_order()
        return order_id

    def add_note(self, order_id: Optional[str], note: str) -> str:
        order_id = self._ensure_order_id(order_id=order_id)
        self.clover_service.add_note_to_order(order_id, note)
        return order_id

    def add_customer_to_order(
        self, order_id: Optional[str], first_name: str, last_name: str,
    ) -> Tuple[str, str]:
        order_id = self._ensure_order_id(order_id=order_id)
        customer_id = self.clover_service.create_customer(
            first_name=first_name, last_name=last_name,
        )
        self.clover_service.add_customer_to_order(
            order_id=order_id, customer_id=customer_id,
        )
        return customer_id, order_id

    def add_line_item(self, inventory_item_id: str, order_id: Optional[str]) -> str:
        order_id = self._ensure_order_id(order_id=order_id)
        self.clover_service.add_line_item(
            order_id=order_id, inventory_item_id=inventory_item_id,
        )
        return order_id

    def calculate_order_total(self, order_id: str) -> int:
        line_items = self.clover_service.get_line_items_for_order(order_id=order_id)
        total = 0
        for line_item in line_items:
            total += line_item["price"]
        return total

    def mark_order_as_paid(self, order_id: str, stripe_reference: str) -> None:
        self.clover_service.pay_for_order(
            order_id=order_id, stripe_reference=stripe_reference,
        )


_DEFAULT_ORDER_CORE_SERVICE: Optional[OrderCoreService] = None


def default_order_core_service() -> OrderCoreService:
    global _DEFAULT_ORDER_CORE_SERVICE
    if _DEFAULT_ORDER_CORE_SERVICE is None:
        _DEFAULT_ORDER_CORE_SERVICE = OrderCoreService()
    return _DEFAULT_ORDER_CORE_SERVICE
