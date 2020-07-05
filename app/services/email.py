from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from typing import Optional
from urllib import request

from app.settings import GMAIL_PASSWORD
from app.settings import GMAIL_USER
from app.settings import RECEIPT_URL_PREFIX


def default_email_client() -> SMTP_SSL:
    return SMTP_SSL("smtp.gmail.com", 465)


class EmailService:

    FROM_ADDRESS = "orders@wicksonrestaurant.com"

    def _init_email(self) -> None:
        self.email_client = default_email_client()
        self.email_client.login(GMAIL_USER, GMAIL_PASSWORD)

    def _create_email_body(
        self, customer_email_address: str, order_id: str,
    ) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Order {order_id} Receipt"
        msg["From"] = self.FROM_ADDRESS
        msg["To"] = customer_email_address
        msg.attach(MIMEText(self._get_receipt(order_id=order_id), "html"))
        return msg

    def _get_receipt(self, order_id: str) -> str:
        fp = request.urlopen(RECEIPT_URL_PREFIX + order_id)
        receipt_bytes = fp.read()

        receipt = receipt_bytes.decode("utf8")
        fp.close()
        return receipt

    def send_email(self, customer_email_address: str, order_id: str) -> None:
        self._init_email()
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
