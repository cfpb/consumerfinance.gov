#!/usr/bin/env python

from django.contrib import admin

from paying_for_college.models import (
    Alias,
    ConstantCap,
    ConstantRate,
    Contact,
    Feedback,
    Nickname,
    Program,
    School,
)


class ConstantRateAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "note", "value", "updated")
    list_editable = ["value"]


class ConstantCapAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "note", "value", "updated")
    list_editable = ["value"]


class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "primary_alias",
        "school_id",
        "operating",
        "city",
        "state",
        "settlement_school",
    )
    list_filter = ("settlement_school", "operating", "state")
    list_editable = ("settlement_school",)
    search_fields = ["school_id", "city", "state"]
    ordering = ["state"]


class AliasAdmin(admin.ModelAdmin):
    list_display = ("alias", "institution", "is_primary")
    search_fields = ["alias"]


class NicknameAdmin(admin.ModelAdmin):
    list_display = ("nickname", "institution", "is_female")
    search_fields = ["nickname"]


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "contacts", "endpoint")


admin.site.register(ConstantRate, ConstantRateAdmin)
admin.site.register(ConstantCap, ConstantCapAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Feedback)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Nickname, NicknameAdmin)
admin.site.register(Program)
