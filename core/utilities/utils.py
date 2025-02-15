

import logging
import random
import sys
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, get_connection

import environ
env = environ.Env()
environ.Env.read_env('.env')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def generate_code():
    return "".join(random.choice("0123456789") for i in range(5))


def generate_random_chars(number=10):
    """
    Return a 10 character random string usable as a slug.
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(chars) for i in range(number))

    
def send_email_register_verification_code(data):
    context = {
        "greeting_to": f"Hi {data['greeting_to']}",
        "email_body": "Welcome aboard! \nUse the code below to verify your email for your Ayadata Tast Management Account.",
        "verify_code": data["verify_code"],
        "receipient_email": data["email_to"],
        "subject": "Ayadata Task API - Account Activation",
    }
    mailTemplate = get_template("account/email_register_verification.html").render(
        context
    )
    email = EmailMultiAlternatives(
        subject="Ayadata Task API - Account Activation", body=" ", to=[data["email_to"]]
    )
    email.attach_alternative(mailTemplate, "text/html")
    email.send()
    
def send_email_verification_code(data):
    context = {
        "email_body": "Welcome aboard 😊!\n Use the code below to verify your email for your Ayadata Task API to be activated. Please note that your verification code will expire after 24hrs",
        "verify_code": data["verify_code"],
        "receipient_email": data["email_to"],
        "subject": "Ayadata Task API - Account Activation",
    }
    mailTemplate = get_template("account/email_verification.html").render(context)
    email = EmailMultiAlternatives(
        subject="Ayadata Task API - Account Activation", body=" ", to=[data["email_to"]]
    )
    email.attach_alternative(mailTemplate, "text/html")
    email.send()
    