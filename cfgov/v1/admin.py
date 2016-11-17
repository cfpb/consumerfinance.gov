from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models.snippets import Contact

from v1.email import send_password_reset_email
from v1.models import Feedback


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(UserAdmin):
    actions = UserAdmin.actions + ['send_password_reset_email']

    def send_password_reset_email(self, request, queryset):
        for user in queryset:
            send_password_reset_email(user.email, request=request)
        self.message_user(
            request,
            '{} password reset email(s) sent'.format(queryset.count())
        )

    send_password_reset_email.short_description = 'Send password reset email'


def feedback_page_url(feedback):
    if feedback.page:
        return feedback.page.url

feedback_page_url.short_description = 'Page URL'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ('submitted_on', 'page__title',)
    list_display = (
        'referrer',
        'comment',
        feedback_page_url,
        'submitted_on',
        'is_helpful'
    )
    search_fields = ['referrer', 'comment']
