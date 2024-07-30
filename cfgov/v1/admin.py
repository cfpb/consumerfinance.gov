from django.contrib import admin

from v1.models import Contact, PortalCategory, PortalTopic


admin.site.register(Contact)

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
