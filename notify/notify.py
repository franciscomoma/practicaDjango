import json
from notify.publisher import publish


def send_email(email_address, subject, message):
    email = {
        'to': str(email_address),
        'subject': str(subject),
        'message': str(message)
    }

    publish('emails', json.JSONEncoder().encode(email))
