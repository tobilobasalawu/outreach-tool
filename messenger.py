from twilio.rest import Client
import config

MESSAGE_TEMPLATE = (
    "Hey, I came across {name} on Google and took the liberty of redesigning "
    "your website. I think it could help you attract a lot more customers. "
    "Want me to send it over? No obligation at all"
)


def send_whatsapp(name: str, phone: str) -> bool:
    try:
        client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
        client.messages.create(
            body=MESSAGE_TEMPLATE.format(name=name),
            from_=config.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{phone}",
        )
        return True
    except Exception as e:
        print(f"[messenger] failed to send to {phone}: {e}")
        return False
