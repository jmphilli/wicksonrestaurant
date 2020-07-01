from email.message import EmailMessage
from smtplib import SMTP_SSL
from typing import Optional

from app.settings import GMAIL_PASSWORD
from app.settings import GMAIL_USER

DEFAULT_EMAIL_CLIENT: Optional[SMTP_SSL] = None


def _default_email_client() -> SMTP_SSL:
    global DEFAULT_EMAIL_CLIENT
    if not DEFAULT_EMAIL_CLIENT:
        DEFAULT_EMAIL_CLIENT = SMTP_SSL("smtp.gmail.com", 465)
    return DEFAULT_EMAIL_CLIENT


class EmailService:

    FROM_ADDRESS = "orders@wicksonrestaurant.com"

    def __init__(self, email_client: Optional[SMTP_SSL] = None) -> None:
        self.email_client = email_client or _default_email_client()
        self.email_client.login(GMAIL_USER, GMAIL_PASSWORD)
        return

    def _create_email_body(
        self, customer_email_address: str, order_id: str,
    ) -> EmailMessage:
        msg = EmailMessage()
        msg.set_content("This is my message")

        msg["Subject"] = f"Order {order_id} Receipt"
        msg["From"] = self.FROM_ADDRESS
        msg["To"] = customer_email_address
        return msg

    def send_email(self, customer_email_address: str, order_id: str) -> None:
        self.email_client.send_message(
            self._create_email_body(
                customer_email_address=customer_email_address, order_id=order_id,
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
