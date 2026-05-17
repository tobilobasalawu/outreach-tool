import time
from twilio.rest import Client
import config

MESSAGE_TEMPLATE = (
    "Hey, I came across {name} on Google and took the liberty of redesigning "
    "your website. I think it could help you attract a lot more customers. "
    "Want me to send it over? No obligation at all"
)

_MAX_RETRIES = 3
_BACKOFF_BASE = 2  # seconds; doubles each retry: 2s, 4s, 8s


def send_whatsapp(name: str, phone: str, dry_run: bool = False) -> bool:
    """Send a WhatsApp message to a lead.

    Args:
        name: Business name to interpolate into the message template.
        phone: E.164-formatted phone number (e.g. +447911123456).
        dry_run: When True, print what would be sent without hitting Twilio.

    Returns:
        True if the message was sent (or would have been sent in dry_run mode),
        False if all retry attempts failed.
    """
    body = MESSAGE_TEMPLATE.format(name=name)

    if dry_run:
        print(f"[messenger] DRY RUN — would send to {phone}: {body}")
        return True

    client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            client.messages.create(
                body=body,
                from_=config.TWILIO_WHATSAPP_FROM,
                to=f"whatsapp:{phone}",
            )
            return True
        except Exception as e:
            if attempt < _MAX_RETRIES:
                wait = _BACKOFF_BASE ** attempt
                print(
                    f"[messenger] attempt {attempt}/{_MAX_RETRIES} failed for "
                    f"{phone}: {e} — retrying in {wait}s"
                )
                time.sleep(wait)
            else:
                print(
                    f"[messenger] all {_MAX_RETRIES} attempts failed for {phone}: {e}"
                )

    return False
