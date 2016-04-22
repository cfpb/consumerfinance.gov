from django.contrib.auth import User
from wagtail.wagtailcore.models import Page, PageRevision

def run():
    ross = User.objects.get(username='rosskarchner')
    for page in Page.objects.all():
        page.owner = ross
        page.save()
    for revision in PageRevision.objects.all():
        revision.user = ross
        revision.save()

    print 'All your pages belong to Ross now muwhuahuahaha'
