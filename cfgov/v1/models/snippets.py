from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import PreviewableMixin, RevisionMixin

from v1.atomic_elements import molecules
from v1.atomic_elements.molecules import Notification

# We import ReusableTextChooserBlock here because this is where it used to
# live. That caused circular imports when it was imported into models. It's no
# longer imported into models from this file, but there are migrations which
# still look for it here.
from v1.blocks import ReusableTextChooserBlock  # noqa


class ReusableText(RevisionMixin, models.Model):
    title = models.CharField(
        verbose_name="Snippet title (internal only)", max_length=255
    )
    sidefoot_heading = models.CharField(
        blank=True,
        max_length=255,
        help_text='Applies "slug" style heading. '
        "Only for use in sidebars and prefooters "
        '(the "sidefoot"). See '
        "https://cfpb.github.io/design-system/foundation/headings#slug-heading",
    )
    text = RichTextField()
    revisions = GenericRelation(
        "wagtailcore.Revision", related_query_name="email_sign_up"
    )

    def __str__(self):
        return self.title


class Contact(PreviewableMixin, models.Model):
    heading = models.CharField(
        verbose_name=("Heading"),
        max_length=255,
        help_text=("The snippet heading"),
    )
    body = RichTextField(blank=True)

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
        FieldPanel("contact_info"),
    ]

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ["heading"]

    def get_preview_template(self, request, mode_name):
        return "v1/includes/organisms/contact-preview.html"


class EmailSignUp(RevisionMixin, models.Model):
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
            "in order to signup. Provide either this or the GovDelivery code, "
            "but not both."
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
        on_delete=models.SET_NULL,
        help_text=(
            'Choose the page that the "See Privacy Act statement" link '
            'should go to. If in doubt, use "Generic Email Sign-Up '
            'Privacy Act Statement".'
        ),
    )
    revisions = GenericRelation(
        "wagtailcore.Revision", related_query_name="email_sign_up"
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


class ReusableNotification(RevisionMixin, models.Model):
    title = models.CharField(
        max_length=255,
        help_text="For internal reference only; does not appear on the site.",
    )
    content = StreamField(
        [("content", Notification())],
        min_num=1,
        max_num=1,
    )

    def __str__(self):
        return self.title
