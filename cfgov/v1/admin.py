from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from login.email import send_password_reset_email

from v1.models import Contact, PortalCategory, PortalTopic

admin.site.register(Contact)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    actions = UserAdmin.actions + ["send_password_reset_email"]

    def send_password_reset_email(self, request, queryset):
        for user in queryset:
            send_password_reset_email(user.email, request=request)
        self.message_user(
            request, "{} password reset email(s) sent".format(queryset.count())
        )

    send_password_reset_email.short_description = "Send password reset email"


# class AnswerPageInline(admin.TabularInline):
#     from ask_cfpb.models import AnswerPage
#     model = AnswerPage


@admin.register(PortalTopic)
class PortalTopicAdmin(admin.ModelAdmin):
    list_display = ("heading", "heading_es", "askids", "page_count")

    def askids(self, obj):
        pks = sorted(
            set(
                [
                    answerpage.answer_base.pk
                    for answerpage in obj.answerpage_set.all()
                ]
            )
        )
        return ", ".join([str(pk) for pk in pks])

    def page_count(self, obj):
        return str(obj.answerpage_set.count())

    askids.short_description = "Ask IDs"
    page_count.short_description = "Page count"


@admin.register(PortalCategory)
class PortalCategoryAdmin(admin.ModelAdmin):
    list_display = ("heading", "heading_es", "askids", "page_count")

    def askids(self, obj):
        pks = sorted(
            set(
                [
                    answerpage.answer_base.pk
                    for answerpage in obj.answerpage_set.all()
                ]
            )
        )
        return ", ".join([str(pk) for pk in pks])

    def page_count(self, obj):
        return str(obj.answerpage_set.count())

    askids.short_description = "Ask IDs"
    page_count.short_description = "Page count"
