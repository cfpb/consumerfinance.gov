from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey


@register_snippet
class GlossaryTerm(index.Indexed, models.Model):
    name_en = models.CharField(max_length=255, verbose_name="TERM (ENGLISH)")
    definition_en = RichTextField(
        null=True, blank=True, verbose_name="DEFINITION (ENGLISH)"
    )
    anchor_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="ANCHOR SLUG (ENGLISH)",
    )
    answer_page_en = models.ForeignKey(
        "ask_cfpb.AnswerPage",
        on_delete=models.CASCADE,
        related_name="glossary_terms",
        null=True,
        blank=True,
        verbose_name="ANSWER PAGE (ENGLISH)",
    )
    name_es = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="TERM (SPANISH)"
    )
    definition_es = RichTextField(
        null=True, blank=True, verbose_name="DEFINITION (SPANISH)"
    )
    anchor_es = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="ANCHOR SLUG (SPANISH)",
    )
    answer_page_es = models.ForeignKey(
        "ask_cfpb.AnswerPage",
        on_delete=models.CASCADE,
        related_name="glossary_terms_es",
        null=True,
        blank=True,
        verbose_name="ANSWER PAGE (SPANISH)",
    )
    portal_topic = ParentalKey(
        "v1.PortalTopic", related_name="glossary_terms", null=True, blank=True
    )
    search_fields = [
        index.SearchField("name_en", partial_match=True),
        index.SearchField("definition_en", partial_match=True),
        index.SearchField("name_es", partial_match=True),
        index.SearchField("definition_es", partial_match=True),
    ]

    def name(self, language="en"):
        if language == "es":
            return self.name_es
        return self.name_en

    def definition(self, language="en"):
        if language == "es":
            return self.definition_es
        return self.definition_en

    def answer_page_url(self, language="en"):
        if language == "es" and self.answer_page_es:
            return self.answer_page_es.url
        if self.answer_page_en:
            return self.answer_page_en.url
        return None

    def anchor(self, language="en"):
        if language == "es":
            return self.anchor_es
        return self.anchor_en

    def __str__(self):
        return self.name_en

    class Meta:
        unique_together = ["portal_topic", "name_en"]
