from axes.utils import reset as axes_reset

from login.models import PasswordHistoryItem


def user_save_callback(sender, **kwargs):
    user = kwargs["instance"]

    # If a new user was just created or a user changed their password,
    # record the user's password in their password history.
    if (
        kwargs["created"]
        or user.password_history.latest().encrypted_password != user.password
    ):
        PasswordHistoryItem.objects.create(
            user=user, encrypted_password=user.password
        )

        # Since the user's password has just been changed successfully,
        # also reset any login lockout if one is associated with the user.
        axes_reset(username=user.username)
