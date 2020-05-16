from typing import Optional

from app.services.clover_gateway import CloverService
from app.services.clover_gateway import default_clover_service


class OrderCoreService:
    def __init__(self, clover_service: Optional[CloverService] = None) -> None:
        self.clover_service = clover_service or default_clover_service()

    def add_line_item(self, inventory_item_id: str, order_id: Optional[str]) -> str:
        if not order_id:
            order_id = self.clover_service.create_order()
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


_DEFAULT_ORDER_CORE_SERVICE: Optional[OrderCoreService] = None


def default_order_core_service() -> OrderCoreService:
    global _DEFAULT_ORDER_CORE_SERVICE
    if _DEFAULT_ORDER_CORE_SERVICE is None:
        _DEFAULT_ORDER_CORE_SERVICE = OrderCoreService()
    return _DEFAULT_ORDER_CORE_SERVICE
