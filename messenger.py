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


def send_sms(name: str, phone: str, dry_run: bool = False) -> bool:
    body = MESSAGE_TEMPLATE.format(name=name)

    if dry_run:
        print(f"[messenger] DRY RUN — would send to {phone}: {body}")
        return True

    client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            client.messages.create(
                body=body,
                messaging_service_sid=config.TWILIO_MESSAGING_SERVICE_SID,
                to=phone,
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
                print(f"[messenger] all {_MAX_RETRIES} attempts failed for {phone}: {e}")

    return False
