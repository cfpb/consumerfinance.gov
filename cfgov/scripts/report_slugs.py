import json
from wagtail.wagtailcore.models import Page, PageRevision
from sheerlike.query import QueryFinder


def run():
    qf = QueryFinder()
    es_reports = qf.reports.search(use_url_arguments=False)
    results = {'successful': [], 'errors': {}, 'multiple_hits': {}}
    for es_report in es_reports:
        try:
            reports = Page.objects.filter(title=es_report.title)
            if len(reports) > 1:
                results['multiple_hits'][str(len(reports))] = es_report.title
                continue
            elif not reports:
                continue
            report = reports.first()
            if report.slug == es_report.slug:
                continue
            old_slug = report.slug
            report.slug = es_report.slug
            report.save()
            revisions = PageRevision.objects.filter(page=report).order_by('id')
            for revision in revisions:
                page_content = json.loads(revision.content_json)
                page_content['slug'] = es_report.slug
                content = json.dumps(page_content)
                revision.content_json = content
                revision.save()
            results['successful'].append(old_slug + ' -- changed to --> ' + report.slug)
        except Exception as e:
            results['errors'][es_report.title] = e
    for key, values in results.iteritems():
        print key
        if type(values) is dict:
            for k, v in values.iteritems():
                print k, ':', v
        else:
            for v in values:
                print v
