from smtplib import SMTP
from typing import Optional

from app.settings import GMAIL_PASSWORD
from app.settings import GMAIL_USER

DEFAULT_EMAIL_CLIENT: Optional[SMTP] = None


def _default_email_client() -> SMTP:
    global DEFAULT_EMAIL_CLIENT
    if not DEFAULT_EMAIL_CLIENT:
        DEFAULT_EMAIL_CLIENT = SMTP("smtp.gmail.com", 587)
    return DEFAULT_EMAIL_CLIENT


class EmailService:

    FROM_ADDRESS = "orders@wicksonrestaurant.com"

    def __init__(self, email_client: Optional[SMTP] = None) -> None:
        self.email_client = email_client or _default_email_client()
        return

    def _create_email_body(self, customer_email_address: str, order_id: str) -> str:
        return """\
        From: %s
        To: %s
        Subject: Order %s

        Order received.
        """ % (
            self.FROM_ADDRESS,
            customer_email_address,
            order_id,
        )

    def send_email(self, customer_email_address: str, order_id: str) -> None:
        self.email_client.ehlo()
        self.email_client.login(GMAIL_USER, GMAIL_PASSWORD)
        self.email_client.sendmail(
            self.FROM_ADDRESS,
            customer_email_address,
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
