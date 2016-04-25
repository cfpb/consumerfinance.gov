from django.contrib.auth import User
from wagtail.wagtailcore.models import Page, PageRevision
from wagtail.wagtaildocs.models import Document
from wagtail.wagtailimages.models import Image
from wagtail.wagtailusers.models import UserProfile

def run():
    ross = User.objects.get(username='rosskarchner')
    for page in Page.objects.all():
        page.owner = ross
        page.save()
    for revision in PageRevision.objects.all():
        revision.user = ross
        revision.save()
    for document in Document.objects.all():
        document.uploaded_by_user = ross
        document.save()
    for image in Image.objects.all():
        image.uploaded_by_user = ross
        image.save()
    for user in UserProfile.objects.all():
        user.user = ross
        user.save()



    print 'All your base belong to Ross now muwhuahuahaha'
