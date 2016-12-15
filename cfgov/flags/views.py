from django.core.exceptions import ImproperlyConfigured
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from wagtail.wagtailcore.models import Site

from .decorators import flag_required
from .forms import FeatureFlagForm, SelectSiteForm, FlagStateForm
from .models import Flag, FlagState
from .utils import init_missing_flag_states_for_site


def select_site(request):
    if request.method == 'POST':
        form = SelectSiteForm(request.POST)

        if form.is_valid():
            site_id = form.cleaned_data['site_id']
            return redirect('flagadmin:list', site_id)
    else:
        default_site = Site.objects.all().filter(is_default_site=True).get()
        return redirect('flagadmin:list', (default_site.id),)


def create(request):
    if request.method == 'POST':
        form = FeatureFlagForm(request.POST)
        if form.is_valid():
            flag = Flag(key=form.cleaned_data['key'])
            flag.save()
            return redirect('flagadmin:select_site')
    else:
        form = FeatureFlagForm()

    context = dict(form=form)
    return render(request, 'flagadmin/flags/create.html', context)


def index(request, site_id):
    sites = Site.objects.all()
    selected_site = Site.objects.get(pk=site_id)

    init_missing_flag_states_for_site(selected_site)
    FlagStateFormSet = modelformset_factory(
        FlagState,
        form=FlagStateForm,
        extra=0
    )

    flagstate_forms = FlagStateFormSet(
        queryset=selected_site.flag_states.all()
    )

    context = {
        'selected_site': selected_site,
        'sites': sites,
        'flagforms': flagstate_forms,
    }

    return render(request, 'flagadmin/index.html', context)


def save(request, site_id):
    if request.method == 'POST':
        selected_site = Site.objects.get(pk=site_id)
        FlagStateFormSet = modelformset_factory(
            FlagState,
            form=FlagStateForm,
            extra=0
        )

        formset = FlagStateFormSet(request.POST)
        if formset.is_valid():
            formset.save()

        # this doesn't address what happens if the formset is invalid
        # index+save should probably be refactored as a single CBV
        return redirect('flagadmin:list', (selected_site.id),)


class FlaggedViewMixin(object):
    flag_name = None
    fallback_view = None
    pass_if_set = True

    def dispatch(self, request, *args, **kwargs):
        if self.flag_name is None:
            raise ImproperlyConfigured(
                "FlaggedViewMixin requires a 'flag_name' argument."
            )

        super_dispatch = super(FlaggedViewMixin, self).dispatch

        decorator = flag_required(
            self.flag_name,
            fallback_view=self.fallback_view,
            pass_if_set=self.pass_if_set
        )

        return decorator(super_dispatch)(request, *args, **kwargs)


class FlaggedTemplateView(FlaggedViewMixin, TemplateView):
    pass
