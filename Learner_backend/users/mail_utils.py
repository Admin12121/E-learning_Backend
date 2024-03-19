from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.messages import constants as messages_constants
import os
from decouple import config  

email_messages = []

class Util:
    @staticmethod
    def send_email(data):
        try:
            subject = data['subject']
            body = data['body']
            to_email = data['to_email']
            
            # Using config function from decouple to read environment variables
            from_email = config('EMAIL_FROM')

            if not all([subject, body, to_email, from_email]):
                raise ValueError("Incomplete email data")

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            success_message = f'Email sent successfully to {to_email}'
            print(success_message)

            email_messages.append((messages_constants.SUCCESS, success_message))

        except Exception as e:
            error_message = f'Error sending email: {e}'
            print(error_message)

            email_messages.append((messages_constants.ERROR, error_message))