from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def new_phi(user):

    from .models import PasswordHistoryItem

    now = timezone.now()
    locked_until = now + timedelta(days=1)
    expires_at = now + timedelta(days=90)

    password_history = PasswordHistoryItem(user=user,
            encrypted_password=user.password,
            locked_until = locked_until,
            expires_at = expires_at)

    password_history.save()
    user.temporarylockout_set.all().delete()

def user_save_callback(sender, **kwargs):
    user = kwargs['instance']    

    try:
        current_password_data = user.passwordhistoryitem_set.latest()
    
        if user.password != current_password_data.encrypted_password:
            new_phi(user)

    except ObjectDoesNotExist:
        new_phi(user)
