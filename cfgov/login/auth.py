import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.encoding import smart_str

from mozilla_django_oidc.auth import OIDCAuthenticationBackend


User = get_user_model()

logger = logging.getLogger(__name__)


def username_from_email(email, claims=None):
    """Generate a username for new users from their email address"""
    email_username = smart_str(email.split("@")[0])
    return email_username


def ensure_wagtail_users_group_membership(user):
    """Ensure SSO users can access the Wagtail admin"""
    # All SSO users will belong to a group that can log into the admin
    try:
        group = Group.objects.get(name="Wagtail Users")
    except Group.DoesNotExist:
        return

    if not user.groups.contains(group):
        logger.debug(f"Adding {user.email} to {group.name}.")
        user.groups.add(group)


def process_roles_admin(user, roles):
    """Adjust a user's is_superuser property based on OIDC roles claim"""
    if settings.OIDC_OP_ADMIN_ROLE is None:
        return

    is_admin = settings.OIDC_OP_ADMIN_ROLE in roles

    if is_admin and not user.is_superuser:
        logger.debug(f"Setting is_superuser for {user.email}.")
        user.is_superuser = True
        return True
    elif not is_admin and user.is_superuser:
        logger.debug(f"Removing is_superuser from {user.email}.")
        user.is_superuser = False
        return True


def process_roles_claim(user, roles):
    """Adjust is_superuser and user group assignment based on OIDC roles"""
    # All SSO users get access to the Wagtail admin.
    # This function does not modify user objects directly, only group
    # membership.
    ensure_wagtail_users_group_membership(user)

    # Specific users should have superuser status based on the contents of
    # their roles
    user_modified = process_roles_admin(user, roles)
    return bool(user_modified)


def process_given_name_claim(user, given_name):
    """Set a Django user's first_name to an OIDC given_name"""
    if user.first_name != given_name:
        logger.info(f"Setting {user.email}'s first name to {given_name}")
        user.first_name = given_name
        return True


def process_family_name_claim(user, family_name):
    """Set a Django user's last_name to an OIDC family_name"""
    if user.last_name != family_name:
        logger.info(f"Setting {user.email}'s last name to {family_name}")
        user.last_name = family_name
        return True


class CFPBOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def get_userinfo(self, access_token, id_token, payload):
        # Roles are part of the parent payload here, and not the userinfo.
        # Preserve them if we can.
        roles = payload.get("roles", [])
        userinfo = super().get_userinfo(access_token, id_token, payload)
        userinfo["roles"] = roles
        return userinfo

    def process_claims(self, user, claims):
        """Run a configured callable for each OIDC claim received

        If a claim processor modifies a user it should return True, and the
        user will be saved once all claims are processed.
        """
        user_modified = False

        claim_processors = {
            "roles": process_roles_claim,
            "given_name": process_given_name_claim,
            "family_name": process_family_name_claim,
        }

        for claim, processor in claim_processors.items():
            if claim not in claims:
                continue

            user_modified |= bool(processor(user, claims[claim]))

        if user_modified:
            logger.info(f"{user.email} changed by claims processors, saving")
            user.save()

        return user

    def update_user(self, user, claims):
        """Update user access based on claims"""
        user = super().update_user(user, claims)
        return self.process_claims(user, claims)

    def create_user(self, claims):
        """Return object for a newly created user account."""
        try:
            user = super().create_user(claims)
        except Exception:
            # If there's an error creating the user (username collision, for
            # example), provide the user with a message and the exception
            # message to help in debugging.
            msg = f"There was an error creating a user for {claims['email']}"
            logger.exception(msg)
            messages.error(self.request, msg)
            return None

        logger.info(f"Created a user for {claims['email']}")
        return self.update_user(user, claims)
