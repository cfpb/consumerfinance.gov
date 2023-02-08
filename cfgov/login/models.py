from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# keep encrypted passwords around to ensure that user does not re-use
# any of the previous 10
class PasswordHistoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # password becomes invalid at...
    locked_until = models.DateTimeField()  # password cannot be changed until
    encrypted_password = models.CharField(_("password"), max_length=128)

    class Meta:
        get_latest_by = "created"

    def can_change_password(self):
        now = timezone.now()
        return now > self.locked_until


# User Failed Login Attempts
class FailedLoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # comma-separated timestamp values, right now it's a 10 digit number,
    # so we can store about 91 last failed attempts
    failed_attempts = models.CharField(max_length=1000)

    def clean_attempts(self, timestamp):
        """Leave only those that happened after <timestamp>"""
        attempts = self.failed_attempts.split(",")
        self.failed_attempts = ",".join(
            [fa for fa in attempts if int(fa) >= timestamp]
        )

    def failed(self, timestamp):
        """Add another failed attempt"""
        attempts = (
            self.failed_attempts.split(",") if self.failed_attempts else []
        )
        attempts.append(str(int(timestamp)))
        self.failed_attempts = ",".join(attempts)

    def too_many_attempts(self, value, timestamp):
        """Compare number of failed attempts to <value>"""
        self.clean_attempts(timestamp)
        attempts = self.failed_attempts.split(",")
        return len(attempts) > value


class TemporaryLockout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
