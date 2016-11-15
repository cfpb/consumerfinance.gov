from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpRequest
from django.http import Http404
from django.db.models import Count, Min, Max
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.context_processors import csrf
from django.utils import timezone

from flags.views import FlaggedViewMixin
from jobmanager.models import Job, FellowshipUpdateList


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


class JobListView(FlaggedViewMixin, ListView):
    model = Job
    ordering = ('close_date', 'title')

    def get_queryset(self):
        qs = super(JobListView, self).get_queryset()
        today = timezone.now().date()
        return qs.filter(
            open_date__lte=today,
            close_date__gte=today,
            active=True
        )


class IndexView(JobListView):
    context_object_name = 'newest_careers'
    template_name = 'about-us/careers/index.html'
    jobs_to_show = 5

    def get_queryset(self):
        return super(IndexView, self).get_queryset()[:self.jobs_to_show]


class CurrentOpeningsView(JobListView):
    context_object_name = 'careers'
    template_name = 'about-us/careers/current-openings/index.html'
