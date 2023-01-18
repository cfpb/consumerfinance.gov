from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet

from v1.atomic_elements import molecules

# We import ReusableTextChooserBlock here because this is where it used to
# live. That caused circular imports when it was imported into models. It's no
# longer imported into models from this file, but there are migrations which
# still look for it here.
from v1.blocks import ReusableTextChooserBlock  # noqa


@register_snippet
class ReusableText(models.Model):
    title = models.CharField(
        verbose_name="Snippet title (internal only)", max_length=255
    )
    sidefoot_heading = models.CharField(
        blank=True,
        max_length=255,
        help_text='Applies "slug" style heading. '
        "Only for use in sidebars and prefooters "
        '(the "sidefoot"). See '
        "[GHE]/flapjack/Modules-V1/wiki/Atoms#slugs",
    )
    text = RichTextField()

    def __str__(self):
        return self.title


@register_snippet
class Contact(models.Model):
    heading = models.CharField(
        verbose_name=("Heading"),
        max_length=255,
        help_text=("The snippet heading"),
    )
    body = RichTextField(blank=True)
    body_shown_in_expandables = models.BooleanField(default=False)

    contact_info = StreamField(
        [
            ("email", molecules.ContactEmail()),
            ("phone", molecules.ContactPhone()),
            ("address", molecules.ContactAddress()),
            ("hyperlink", molecules.ContactHyperlink()),
        ],
        blank=True,
    )

    panels = [
        FieldPanel("heading"),
        FieldPanel("body"),
        FieldPanel("body_shown_in_expandables"),
        FieldPanel("contact_info"),
    ]

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ["heading"]


@register_snippet
class RelatedResource(models.Model):
    title = models.CharField(max_length=255)
    title_es = models.CharField(max_length=255, blank=True, null=True)
    text = RichTextField(blank=True, null=True)
    text_es = RichTextField(blank=True, null=True)

    def trans_title(self, language="en"):
        if language == "es":
            return self.title_es or ""
        return self.title or ""

    def trans_text(self, language="en"):
        if language == "es":
            return self.text_es or ""
        return self.text or ""

    def __str__(self):
        return self.title


@register_snippet
class EmailSignUp(models.Model):
    topic = models.CharField(
        verbose_name="Topic name (internal only)",
        max_length=255,
        null=True,
        blank=True,
    )
    code = models.TextField(
        verbose_name="GovDelivery Code",
        null=True,
        blank=True,
        help_text=(
            "GovDelivery Code (USCFPB_###) for the list people who submit "
            "the form will sign up for. Provide either this or the signup "
            "URL, but not both."
        ),
    )
    url = models.URLField(
        verbose_name="GovDelivery URL",
        null=True,
        blank=True,
        help_text=(
            "URL for the GovDelivery signup page people will be linked to "
            "in order to signup. Provide either this or the signup "
            "URL, but not both."
        ),
    )
    heading = models.TextField(blank=True, default="Stay informed")
    default_heading = models.BooleanField(
        null=True,
        blank=True,
        default=True,
        verbose_name="Default heading style",
        help_text=(
            "If selected, heading will be styled as an H5 "
            "with green top rule. Deselect to style header as H3."
        ),
    )
    text = RichTextField(
        blank=True,
        help_text=(
            "Write a sentence or two about what kinds of emails the "
            "user is signing up for, how frequently they will be sent, "
            "etc."
        ),
    )
    disclaimer_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="Privacy Act statement",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text=(
            'Choose the page that the "See Privacy Act statement" link '
            'should go to. If in doubt, use "Generic Email Sign-Up '
            'Privacy Act Statement".'
        ),
    )

    panels = [
        FieldPanel("topic"),
        FieldPanel("code"),
        FieldPanel("url"),
        FieldPanel("heading"),
        FieldPanel("text"),
        FieldPanel("disclaimer_page"),
    ]

    def __str__(self):
        return (
            f"{self.topic} ({self.url if self.url is not None else self.code})"
        )
