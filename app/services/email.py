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

    def _currency_string(self, val: int) -> str:
        major_units = val / 100
        return f"${major_units:.2f}"

    def _get_receipt(self, order_id: str, order_details: Dict[str, Any]) -> str:
        tax_str = self._currency_string(order_details["tax"])
        total_str = self._currency_string(order_details["total_cost"])
        service_str = self._currency_string(order_details["service_charge"])
        tip_str = ""
        if order_details["tip"] != 0:
            formatted_tip = self._currency_string(order_details["tip"])
            tip_str = f"<h2> Tip </h2> {formatted_tip}"
        line_items = ""
        line_item_aggregation: Dict[str, Any] = {}
        for li in order_details["line_items"]:
            item_id = li["item_id"]
            if li["name"] == "tip":
                continue
            if not line_item_aggregation.get(li["item_id"]):
                line_item_aggregation[item_id] = {
                    "name": li["name"],
                    "price": 0,
                    "quantity": 0,
                }
            line_item_aggregation[item_id]["price"] += li["price"]
            line_item_aggregation[item_id]["quantity"] += 1
        for _, values in line_item_aggregation.items():
            price_str = self._currency_string(values["price"])
            line_items += (
                f"<div>{values['name']} x {values['quantity']} : {price_str}</div>"
            )
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

        <h2>Wickson Restaurant</h2>
        <p class="footer-text">
            <a href="tel:707-895-2955">
                707-895-2955
            </a>
        </p>
        <p class="footer-text">
            <a href="https://www.google.com/maps/place/9000+CA-128,+Philo,+CA+95466/@39.0595109,-123.437016,17z">
                9000 Highway 128, Philo, CA. 95466
            </a>
        </p>
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
