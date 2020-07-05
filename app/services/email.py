from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from typing import Any
from typing import Dict
from typing import Optional

from app.settings import GMAIL_PASSWORD
from app.settings import GMAIL_USER


def default_email_client() -> SMTP_SSL:
    return SMTP_SSL("smtp.gmail.com", 465)


class EmailService:

    FROM_ADDRESS = "orders@wicksonrestaurant.com"

    def _init_email(self) -> None:
        self.email_client = default_email_client()
        self.email_client.login(GMAIL_USER, GMAIL_PASSWORD)

    def _create_email_body(
        self, customer_email_address: str, order_id: str, order_details: Dict[str, Any],
    ) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Order {order_id} Receipt"
        msg["From"] = self.FROM_ADDRESS
        msg["To"] = customer_email_address
        msg.attach(
            MIMEText(
                self._get_receipt(order_id=order_id, order_details=order_details),
                "html",
            ),
        )
        return msg

    def _get_receipt(self, order_id: str, order_details: Dict[str, Any]) -> str:
        tax_str = "$" + str(order_details["tax"])
        total_str = "$" + str(order_details["total"])
        service_str = "$" + str(order_details["service_charge"])
        tip_str = ""
        if order_details["tip"] != 0:
            tip_str = f"<h2> Tip </h2> {order_details['tip']}"
        line_items = ""
        line_item_aggregation: Dict[str, Any] = {}
        for li in order_details["line_items"]:
            if not line_item_aggregation.get(li["item_id"]):
                line_item_aggregation["item_id"] = {
                    "name": li["name"],
                    "price": 0,
                    "quantity": 0,
                }
            line_item_aggregation["item_id"]["price"] += li["price"]
            line_item_aggregation["item_id"]["quantity"] += 1
        for _, values in line_item_aggregation.items():
            line_items += f"<div>{values['name']} x {values['quantity']} : {values['price']}</div>"
        receipt = """
        <html>
        <body>
        <h1> Order {order_id} </h1>
        {line_items}
        <h3> Service Charge <h3>
        {service_str}
        {tip_str}
        <h3> Tax </h3>
        {tax_str}
        <h2> Total </h2>
        {total_str}
        </body>
        </html>
        """.format(
            order_id=order_id,
            line_items=line_items,
            service_str=service_str,
            tip_str=tip_str,
            total_str=total_str,
            tax_str=tax_str,
        )
        return receipt

    def send_email(
        self, customer_email_address: str, order_id: str, order_details: Dict[str, Any],
    ) -> None:
        self._init_email()
        self.email_client.send_message(
            self._create_email_body(
                customer_email_address=customer_email_address,
                order_id=order_id,
                order_details=order_details,
            ),
        )
        self.email_client.close()
        return


DEFAULT_EMAIL_SERVICE: Optional[EmailService] = None


def default_email_service() -> EmailService:
    global DEFAULT_EMAIL_SERVICE
    if DEFAULT_EMAIL_SERVICE is None:
        DEFAULT_EMAIL_SERVICE = EmailService()
    return DEFAULT_EMAIL_SERVICE
