import sys
import os.path
from unipath import Path
import codecs
import json
import traceback
from importlib import import_module

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied, ValidationError, ObjectDoesNotExist
from django.contrib.messages.api import MessageFailure

from wagtail.wagtailadmin.views.pages import create
from wagtail.wagtailcore.models import Page


class Command(BaseCommand):
    help = "populate a Django model using a Sheer indexer"

    def add_arguments(self, parser):
        parser.add_argument('wp_type')
        parser.add_argument('wagtail_type')
        parser.add_argument('parent_page_slug')
        parser.add_argument('-u', '--username', action='store', required=True)
        parser.add_argument('-p', '--password', action='store', required=True)
        parser.add_argument('--app', action='store', default='v1')

    def handle(self, *args, **options):
        wp_type = options['wp_type']
        wagtail_type = options['wagtail_type']
        parent_page_slug = options['parent_page_slug']
        username = options['username']
        password = options['password']
        app = options['app']

        sheer_sites = settings.SHEER_SITES
        sheer_libs = [Path(s).child('_lib') for s in sheer_sites]
        sys.path += sheer_libs

        processors = {}

        possible_processor_configs = \
            [Path(s).child('_settings').child('processors.json')
             for s in sheer_sites]

        for procjson in possible_processor_configs:
            if os.path.exists(procjson):
                with codecs.open(procjson, encoding='utf8') as jsonfile:
                    raw_json = jsonfile.read()
                    merged_json = os.path.expandvars(raw_json)
                    config = json.loads(merged_json)
                    processors.update(config)

        if wp_type in processors:
            mod = import_module(processors[wp_type]['processor'])
            generator = mod.documents(wp_type, **processors[wp_type])
            try:  # to import the module from the arg: wagtail_type
                wagtail_type_module = __import__('processors.%s' % wagtail_type,
                                                 globals(), locals(),
                                                 [wp_type])
            except ImportError:
                raise ImportError("No module found in .helpers for name (%s)"
                                  % wp_type)
            results = {
                'migrated': 0,
                'existed': 0,
                'errors': 0,
                'migrated_slugs': [],
                'existed_slugs': [],
                'errors_slugs': [],
            }
            for doc in generator:
                # Map the document to the given model name
                results = migrate(doc['_source'], username, password,
                                  parent_page_slug, wagtail_type_module, app,
                                  wagtail_type, results)

            for state in ['migrated', 'existed', 'errors']:
                print "%s %s" % (results[state], state)
                if options['verbosity'] > 1:
                    for slug in results[state + '_slugs']:
                        print slug
        else:
            raise CommandError('could not find a processor for %s' % wp_type)


def migrate(doc, username, password, parent_page_slug, module, app, wagtail_type, results):
    request = HttpRequest()
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active and user.is_superuser:
            request.user = user
        else:
            raise PermissionDenied('This user does not have permissions to perform this operation')
    else:
        # the authentication system was unable to verify the username and password
        raise ValidationError("The username and password were incorrect.")

    ### Check to see if the post already exists. We don't want WP data overwriting anything
    if Page.objects.filter(slug=doc.get('slug')).exists():
        results['existed'] += 1
        results['existed_slugs'].append(doc.get('slug'))
        return results

    ### Get parent. If parent doesn't exist, then raise DoesNotExist
    try:
        parent = Page.objects.get(slug=parent_page_slug)
    except:
        raise ObjectDoesNotExist('Parent page does not exist')

    # Convert the document data into Wagtail readable data then publish it.
    request.POST = module.convert(doc)
    request.POST['action-publish'] = u'Publish on WWW'

    try:  # Create the page. Since we aren't hitting the middleware we have to catch the MessageFailure exception
        create(request, app, wagtail_type, parent.id)
    except MessageFailure:
        if 'messages.error' in traceback.format_exc():
            print 'Couldn\'t save page with slug: %s' % doc.get('slug')
            results['errors'] += 1
            results['errors_slugs'].append(doc.get('slug'))
            return results
        results['migrated'] += 1
        results['migrated_slugs'].append(doc.get('slug'))
        return results
