from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_verified)


generate_token = TokenGenerator()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Verify Email"
    email_body = render_to_string('email/verify_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    send_mail(
        email_subject,
        email_body,
        'verification@localhost.com',
        [user.email]
    )
