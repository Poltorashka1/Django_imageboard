from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    """Создания токена для активации аккаунта"""

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_confirm)
        )


# class PasswordResetToken(PasswordResetTokenGenerator):
#     """Не используется"""
#
#     def _make_hash_value(self, user, timestamp):
#         return (
#                 six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.reset_password)
#         )


account_activation_token = TokenGenerator()
# password_reset_token = PasswordResetToken()
