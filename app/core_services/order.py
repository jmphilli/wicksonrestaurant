from typing import Optional

from app.services.clover_gateway import CloverService
from app.services.clover_gateway import default_clover_service


class OrderCoreService:
    def __init__(self, clover_service: Optional[CloverService]) -> None:
        self.clover_service = clover_service or default_clover_service()

    def calculate_order_total(self, order_id: str) -> int:
        line_items = self.clover_service.get_line_items_for_order(order_id=order_id)
        total = 0
        for line_item in line_items:
            total += line_item["price"]
        return total
