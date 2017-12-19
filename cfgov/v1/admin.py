from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from wagtail.wagtailcore.models import Page

from v1.email import send_password_reset_email
from v1.models import Contact, Feedback


admin.site.register(Contact)
admin.site.unregister(User)
admin.site.unregister(Page)


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


def feedback_page_title(feedback):
    if feedback.page:
        return feedback.page.title

feedback_page_title.short_description = 'Page'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    actions = ['export_selection_as_csv']

    def export_selection_as_csv(self, request, queryset):
        object_name = queryset.model._meta.object_name
        user = request.user
        subject = "CFPB website {} download"
        message = 'A CSV file of selected {} records is attached.'
        fromline = 'do-not-reply@cfpb.gov'
        user_message = "Sent {} selected {} records as CSV to {}"
        recipients = [user.email]
        csvfile = Feedback().assemble_csv(queryset)
        email = EmailMessage(
            subject.format(object_name),
            message.format(object_name),
            fromline,
            recipients
        )
        email.attach('Feedbacks.csv', csvfile)
        email.send()
        self.message_user(
            request,
            user_message.format(
                queryset.count(),
                object_name,
                ", ".join(recipients)
            )
        )

    export_selection_as_csv.short_description = 'Export selection as CSV'

    list_filter = ('submitted_on', 'language')
    list_display = (
        'submitted_on',
        feedback_page_title,
        'referrer',
        'is_helpful',
        'comment',
        'email',
        'language'
    )
    search_fields = ['referrer', 'comment', 'page__title']
