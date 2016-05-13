from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpRequest
from django.http import Http404
from django.db.models import Count, Min, Max
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.utils import timezone
import re
import datetime

from jobmanager.models import Job, JobCategory, Location, FellowshipUpdateList



@csrf_exempt
def fellowship_form_submit(request):
    if request.POST:
        P = request.POST
        FellowshipUpdateList(
            email = P.get('email'),
            first_name = P.get('first_name'),
            last_name = P.get('last_name'),
            likes_design = bool(P.get('likes_design', False)),
            likes_cybersecurity = bool(P.get('likes_cybersecurity', False)),
            likes_development = bool(P.get('likes_development', False)),
            likes_data = bool(P.get('likes_data', False)),
        ).save()

    return HttpResponse('OK')

def index(request):
    today = timezone.now().date()
    jobs = Job.objects.filter(open_date__lte=today,close_date__gte=today,           
            active=True).order_by('-open_date')[:5]
    
    context = {'newest_careers':jobs}
    return render(request, "about-us/careers/index.html", context)


def detail(request, pk=None, slug=None):
    today = timezone.now().date()

    qs = Job.objects.filter(open_date__lte=today,
                close_date__gte=today,active=True)
    if pk:
        job = get_object_or_404(qs, pk=pk)

        return redirect(job.get_absolute_url())

    if slug:
        job = get_object_or_404(qs, slug=slug)
    salary_min = int(job.salary_min or min([g.salary_min 
        for g in job.grades.all()]))
    salary_max = int(job.salary_max or max([g.salary_max
        for g in job.grades.all()]))

    return render(request, "about-us/careers/_single.html",
        {'career':job,
            'salary_min': salary_min,
            'salary_max': salary_max})


def current_openings(request):
    today = datetime.date.today()

    today = timezone.now().date()
    jobs = Job.objects.filter(open_date__lte=today,close_date__gte=today,           
            active=True).order_by('close_date','title')
    
    return render(request, "about-us/careers/current-openings/index.html",
        {'careers':jobs})


# This function is used to submit to Gov-Delivery
@csrf_exempt
def submit_govdelivery(request):
    code = request.POST.get('code')
    email = request.POST.get('email')
    import urllib
    try:
        res = urllib.urlopen('https://public.govdelivery.com/service/process_ss.xml?code=%s&email=%s' % (code, email))
    except:
        # todo: log error
        res = '<response code="500" message="Unknown Server Error"/>'

    return HttpResponse(res, content_type="application/xhtml+xml")
