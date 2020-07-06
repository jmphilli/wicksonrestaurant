import math
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from app.constants import STRIPE_FIXED_COST
from app.constants import STRIPE_VARIABLE_COST
from app.constants import TAX_RATE
from app.services.clover_gateway import CloverService
from app.services.clover_gateway import default_clover_service
from app.services.email import default_email_service
from app.services.email import EmailService


class OrderCoreService:
    def __init__(
        self,
        clover_service: Optional[CloverService] = None,
        email_service: Optional[EmailService] = None,
    ) -> None:
        self.clover_service = clover_service or default_clover_service()
        self.email_service = email_service or default_email_service()

    def _ensure_order_id(self, order_id: Optional[str]) -> str:
        if not order_id:
            return self.clover_service.create_order()
        return order_id

    def add_customer_to_order(
        self,
        order_id: Optional[str],
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        note: Optional[str],
    ) -> Tuple[str, str]:
        order_id = self._ensure_order_id(order_id=order_id)
        customer_id = self.clover_service.create_customer(
            first_name=first_name, last_name=last_name, email=email, phone=phone,
        )
        self.clover_service.add_customer_to_order(
            order_id=order_id, customer_id=customer_id,
        )
        if note:
            self.clover_service.add_note_to_order(order_id, note)
        return customer_id, order_id

    def get_customer_from_order(self, order_id: str) -> Dict[str, Any]:
        order = self.clover_service.get_order(order_id=order_id)
        customer_id = order.get("customers", {}).get("elements", [])[0].get("id")
        customer_dict = {}
        if customer_id:
            customer = self.clover_service.get_customer(customer_id=customer_id)
            email = (
                customer.get("emailAddresses", {})
                .get("elements", [{}])[0]
                .get("emailAddress")
            )
            phone = (
                customer.get("phoneNumbers", {})
                .get("elements", [{}])[0]
                .get("phoneNumber")
            )
            customer_dict = {
                "first_name": customer.get("firstName"),
                "last_name": customer.get("lastName"),
                "email": email,
                "phone": phone,
            }
        return customer_dict

    def add_line_item(self, inventory_item_id: str, order_id: Optional[str]) -> str:
        order_id = self._ensure_order_id(order_id=order_id)
        self.clover_service.add_line_item(
            order_id=order_id, inventory_item_id=inventory_item_id,
        )
        return order_id

    def remove_line_item(self, inventory_item_id: str, order_id: Optional[str]) -> str:
        order_id = self._ensure_order_id(order_id=order_id)
        order_details = self.get_order_details(order_id=order_id)
        line_items = order_details["line_items"]
        if not line_items:
            return order_id
        line_item_id = ""
        for line_item in line_items:
            if line_item["item_id"] == inventory_item_id:
                line_item_id = line_item["id"]
                break
        if not line_item_id:
            return order_id
        self.clover_service.remove_line_item(
            order_id=order_id, line_item_id=line_item_id,
        )
        return order_id

    def add_tip(self, order_id: str, tip_amount: int) -> None:
        line_items = self.clover_service.get_line_items_for_order(order_id=order_id)
        existing_line_item_id = None
        for line_item in line_items:
            if line_item.get("name") == "tip":
                existing_line_item_id = line_item.get("id")
        self.clover_service.add_tip(
            order_id=order_id,
            tip_amount=tip_amount,
            existing_line_item_id=existing_line_item_id,
        )
        return

    def _calculate_total_and_tax(
        self, line_items: List[Dict[str, Any]],
    ) -> Tuple[int, int, int, int]:
        total = 0
        tip_amount = 0
        tip = 0  # default when user doesn't tip
        for line_item in line_items:
            if line_item.get("name") == "tip":
                if line_item["price"] > 0:
                    # it's custom
                    tip_amount = int(line_item["price"])
            else:  # skip adding tip to total until the end
                total += int(line_item["price"])
        if tip_amount:
            tip = tip_amount
        total += STRIPE_FIXED_COST
        service_charge = STRIPE_FIXED_COST
        tax = self._calculate_tax(running_total=total)  # no tip?
        total += tax
        # last one
        stripe_variable_cost = math.ceil(STRIPE_VARIABLE_COST * total)
        total += stripe_variable_cost
        service_charge += stripe_variable_cost
        # add tip - not subject to tax because not a service charge or anything like that
        total += tip
        return total, tip, tax, service_charge

    def _calculate_tax(self, running_total: float) -> int:
        return math.ceil(running_total * TAX_RATE)

    def calculate_order_total(self, order_id: str) -> int:
        line_items = self.clover_service.get_line_items_for_order(order_id=order_id)
        return self._calculate_total_and_tax(line_items)[0]

    def get_order_details(self, order_id: str) -> Dict[str, Any]:
        line_items = self.clover_service.get_line_items_for_order(order_id=order_id)
        total_cost, tip, tax, service_charge = self._calculate_total_and_tax(line_items)
        parsed_line_items = []
        for line_item in line_items:
            parsed_line_items.append(
                {
                    "id": line_item.get("id", 0),
                    "item_id": line_item.get("item", {}).get("id", 0),
                    "name": line_item["name"],
                    "price": line_item["price"],
                },
            )
        return {
            "line_items": parsed_line_items,
            "total_cost": total_cost,
            "tax": tax,
            "tip": tip,
            "service_charge": service_charge,
        }

    def mark_order_as_paid(
        self, order_id: str, stripe_reference: str, total: int,
    ) -> None:
        self.clover_service.pay_for_order(
            order_id=order_id, stripe_reference=stripe_reference, total=total,
        )

    def order_is_paid(self, order_id: str) -> bool:
        order = self.clover_service.get_order(order_id=order_id)
        if order.get("externalReferenceId"):
            return True
        return False

    def send_email(self, order_id: str) -> None:
        customer = self.get_customer_from_order(order_id=order_id)
        order_details = self.get_order_details(order_id=order_id)
        customer_email_address = customer.get("email")
        if customer_email_address:
            self.email_service.send_email(
                customer_email_address=customer_email_address,
                order_id=order_id,
                order_details=order_details,
            )
        return


_DEFAULT_ORDER_CORE_SERVICE: Optional[OrderCoreService] = None


def default_order_core_service() -> OrderCoreService:
    global _DEFAULT_ORDER_CORE_SERVICE
    if _DEFAULT_ORDER_CORE_SERVICE is None:
        _DEFAULT_ORDER_CORE_SERVICE = OrderCoreService()
    return _DEFAULT_ORDER_CORE_SERVICE
