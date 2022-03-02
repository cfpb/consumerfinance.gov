from collections import OrderedDict, namedtuple

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render

from wagtail.core.models import Collection, Page


User = get_user_model()
PagePermissions = namedtuple("PagePermissions", ["page", "group_permissions"])
CollectionPermissions = namedtuple(
    "CollectionPermissions", ["collection", "group_permissions"]
)
CTPermissions = namedtuple(
    "CTPermissions", ["content_type", "group_permissions"]
)


def display_group_roster(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    active_users = group.user_set.filter(is_active=True).order_by("username")
    inactive_users = group.user_set.filter(is_active=False).order_by(
        "username"
    )
    return render(
        request,
        "permissions_viewer/group.html",
        {
            "active_users": active_users,
            "inactive_users": inactive_users,
            "group": group,
        },
    )


def display_user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    pages = Page.objects.filter(group_permissions__group__user=user).distinct()

    page_permissions = []
    groups = list(user.groups.all())
    for page in pages:
        group_perms = [
            group.page_permissions.filter(page=page) for group in groups
        ]
        page_permissions.append(
            PagePermissions(page=page, group_permissions=group_perms)
        )

    collection_permissions = []
    collections = list(
        Collection.objects.filter(
            group_permissions__group__user=user
        ).distinct()
    )

    for collection in collections:
        group_perms = [
            group.collection_permissions.filter(collection=collection)
            for group in groups
        ]
        collection_permissions.append(
            CollectionPermissions(
                collection=collection, group_permissions=group_perms
            )
        )

    groups_content_types = (
        ContentType.objects.filter(permission__group__user=user)
        .distinct()
        .order_by("app_label", "model")
    )

    group_ct_permissions = []
    for ct in groups_content_types:
        group_perms = [
            group.permissions.filter(content_type=ct) for group in groups
        ]
        group_ct_permissions.append(
            CTPermissions(content_type=ct, group_permissions=group_perms)
        )

    users_content_types = (
        ContentType.objects.filter(permission__user=user)
        .distinct()
        .order_by("app_label", "model")
    )
    users_ct_permissions = OrderedDict()
    for content_type in users_content_types:
        users_ct_permissions[content_type] = user.user_permissions.filter(
            content_type=content_type
        )

    return render(
        request,
        "permissions_viewer/user.html",
        {
            "user": user,
            "groups": groups,
            "page_permissions": page_permissions,
            "collection_permissions": collection_permissions,
            "group_ct_permissions": group_ct_permissions,
            "users_ct_permissions": users_ct_permissions,
        },
    )


def index(request):
    active_users = User.objects.filter(is_active=True).order_by("username")
    inactive_users = User.objects.filter(is_active=False).order_by("username")
    groups = Group.objects.all().order_by("name")

    return render(
        request,
        "permissions_viewer/index.html",
        {
            "active_users": active_users,
            "inactive_users": inactive_users,
            "groups": groups,
        },
    )
