from django import forms
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, HelpPanel, InlinePanel, MultiFieldPanel,
    ObjectList, TabbedInterface
)
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.fields import RichTextField
from wagtail.core.models import PageManager, PageQuerySet

from modelcluster.fields import ParentalManyToManyField

from jobmanager.models.django import (
    JobCategory, JobLength, Office, Region, ServiceType
)
from v1.models import CFGOVPage
from v1.models.snippets import ReusableText


class JobListingPageQuerySet(PageQuerySet):
    def open(self):
        today = timezone.now().date()

        return self \
            .filter(live=True) \
            .filter(open_date__lte=today) \
            .filter(close_date__gte=today) \
            .order_by('close_date', 'title')


JobListingPageManager = PageManager.from_queryset(JobListingPageQuerySet)


LOCATION_HELP_TEXT = (
    "Select <strong>either</strong> one or more offices "
    "<strong>or</strong> one or more regions."
)


class JobListingPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        offices = cleaned_data.get('offices')
        has_offices = offices.exists() if offices else False

        regions = cleaned_data.get('regions')
        has_regions = regions.exists() if regions else False

        if (
            (has_offices and has_regions) or
            (not has_offices and not has_regions)
        ):
            self.add_error('regions', mark_safe(LOCATION_HELP_TEXT))

        if has_regions and cleaned_data['allow_remote']:
            self.add_error(
                'allow_remote',
                "Remote option only applies to jobs with office locations."
            )

        return cleaned_data


class JobListingPage(CFGOVPage):
    description = RichTextField('Summary')
    open_date = models.DateField('Open date')
    close_date = models.DateField('Close date')
    salary_min = models.DecimalField(
        'Minimum salary',
        max_digits=11,
        decimal_places=2
    )
    salary_max = models.DecimalField(
        'Maximum salary',
        max_digits=11,
        decimal_places=2
    )
    division = models.ForeignKey(
        JobCategory,
        on_delete=models.PROTECT,
        null=True
    )
    job_length = models.ForeignKey(
        JobLength,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Position length",
        blank=True
    )
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    offices = ParentalManyToManyField(
        Office,
        related_name='job_listings',
        blank=True
    )
    allow_remote = models.BooleanField(
        default=False,
        verbose_name="Office location can also be remote"
    )
    regions = ParentalManyToManyField(
        Region,
        related_name='job_listings',
        blank=True
    )
    responsibilities = RichTextField(
        'Responsibilities',
        null=True,
        blank=True
    )
    travel_required = models.BooleanField(
        blank=False,
        default=False,
        help_text=(
            'Optional: Check to add a "Travel required" section to the '
            'job description. Section content defaults to "Yes".'
        )
    )
    travel_details = RichTextField(
        null=True,
        blank=True,
        help_text='Optional: Add content for "Travel required" section.'
    )
    additional_section_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Optional: Add title for an additional section '
                  'that will display at end of job description.'
    )
    additional_section_content = RichTextField(
        null=True,
        blank=True,
        help_text='Optional: Add content for an additional section '
                  'that will display at end of job description.'
    )

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('division'),
            InlinePanel('grades', label='Grades'),
            FieldRowPanel([
                FieldPanel('open_date', classname='col6'),
                FieldPanel('close_date', classname='col6'),
            ]),
            FieldRowPanel([
                FieldPanel('salary_min', classname='col6'),
                FieldPanel('salary_max', classname='col6'),
            ]),
            FieldRowPanel([
                FieldPanel('service_type', classname='col6'),
                FieldPanel('job_length', classname='col6'),
            ]),
        ], heading='Details'),
        MultiFieldPanel([
            HelpPanel(LOCATION_HELP_TEXT),
            FieldRowPanel([
                FieldPanel('offices', widget=forms.CheckboxSelectMultiple),
                FieldPanel('allow_remote'),
            ]),
            FieldPanel('regions', widget=forms.CheckboxSelectMultiple),
        ], heading='Location'),
        MultiFieldPanel([
            FieldPanel('description'),
            FieldPanel('responsibilities'),
            FieldPanel('travel_required'),
            FieldPanel('travel_details'),
            FieldPanel('additional_section_title'),
            FieldPanel('additional_section_content'),
        ], heading='Description'),
        InlinePanel(
            'usajobs_application_links',
            label='USAJobs application links'
        ),
        InlinePanel(
            'email_application_links',
            label='Email application links'
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    base_form_class = JobListingPageForm

    objects = JobListingPageManager()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        try:
            context['about_us'] = ReusableText.objects.get(
                title='About us (For consumers)'
            )
        except ReusableText.DoesNotExist:
            pass

        context.update({
            'offices': [
                {
                    'name': office.name,
                    'state_id': office.state_id,
                } for office in self.offices.all()
            ],
            'regions': [
                {
                    'name': region.name,
                    'states': [
                        state.abbreviation for state in region.states.all()
                    ],
                    'major_cities': list(
                        region.major_cities.values('name', 'state_id')
                    ),
                } for region in self.regions.all()
            ],
            'grades': list(map(str, self.grades.all())),
        })

        return context

    @property
    def page_js(self):
        return super().page_js + ['summary.js']
