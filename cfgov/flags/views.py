from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import modelformset_factory

from wagtail.wagtailcore.models import Site

from .forms import SelectSiteForm, FlagStateForm
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
	select_site_form = SelectSiteForm
	return redirect('flagadmin:list', (default_site.id),)

def index(request, site_id):
    sites = Site.objects.all()
    selected_site = Site.objects.get(pk=site_id)

    init_missing_flag_states_for_site(selected_site)
    FlagStateFormSet=modelformset_factory(FlagState,
            form=FlagStateForm, extra=0)
    
    flagstate_forms = FlagStateFormSet(
            queryset=selected_site.flagstate_set.all())

    context = {'selected_site':selected_site, 'sites':sites,
            'flagforms':flagstate_forms}

    return render(request,'flagadmin/index.html', context)

def save(request, site_id):
    if request.method == 'POST':
        selected_site = Site.objects.get(pk=site_id)
        FlagStateFormSet=modelformset_factory(FlagState,
                form=FlagStateForm, extra=0)
        formset = FlagStateFormSet(request.POST)
        if formset.is_valid():
            formset.save()

        # this doesn't address what happens if the formset is invalid
        # index+save should probably be refactored as a single CBV
        return redirect('flagadmin:list', (selected_site.id),)
