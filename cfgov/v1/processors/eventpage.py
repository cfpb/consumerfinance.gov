import dateutil

from core.management.commands._helpers import PageDataConverter


class DataConverter(PageDataConverter):
    def convert(self, doc):
        post_dict = {
            'title':      doc.get('title', u''),
            'slug':       doc.get('slug', u''),
            'body':       doc.get('content', u''),
            'flickr_url': doc.get('flickr_url', u''),
        }
        tags = ''
        for tag in doc.get('tags'):
            if ' ' in tag:
                tag = '"%s"' % tag
            tags += tag + ', '
        if tags:
            tags = tags[0:-2]
        post_dict['tags'] = tags
        post_dict['authors'] = '"%s"' % doc.get('author', {}).get('name', '')

        times = [('beginning_time', 'start_dt'), ('ending_time', 'end_dt')]
        for t in times:
            if doc.get(t[0]):
                time = doc.get(t[0]).get('date', u'')
                if time:
                    dt = dateutil.parser.parse(time)
                    post_dict[t[1]] = dt.strftime('%Y-%m-%d %H:%M')

        if doc.get('venue'):
            post_dict['venue_name'] = doc['venue'].get('name', u'')
            if doc['venue'].get('address', u''):
                for info in ['state', 'city', 'street', 'suite', 'zip']:
                    post_dict['venue_'+info] = \
                        doc['venue']['address'].get(info, u'')

        if doc.get('live_stream'):
            for info in ['url', 'available', 'date']:
                post_dict['live_stream_'+info] = doc['live_stream'].get(info,
                                                                        u'')

        for tense in ['archive', 'live', 'future']:
            if doc.get(tense):
                summary = doc[tense].get('summary', u'')
                if 'http://content' in summary:
                    summary = summary.replace('http://content', 'http://www')
                post_dict[tense+'_body'] = summary
                if tense == 'archive':
                    post_dict['flickr_url'] = doc['archive'].get('flickr', u'')
                    post_dict['youtube_url'] = doc['archive'].get('youtube',
                                                                  u'')

        post_dict['agenda_items-count'] = len(doc.get('agenda', u''))
        if doc.get('agenda'):
            for i in range(len(doc.get('agenda', u''))):
                for info in (('order', i), ('type', 'item'), ('deleted', u'')):
                    post_dict['agenda_items-'+str(i)+'-'+info[0]] = info[1]
                times = [('beginning_time', 'start_dt'),
                         ('ending_time', 'end_dt')]
                for t in times:
                    if doc['agenda'][i].get(t[0], u''):
                        time = doc['agenda'][i].get(t[0]).get('date', u'')
                        if time:
                            dt = dateutil.parser.parse(time)
                            post_dict['agenda_items-'+str(i)+'-value-' +
                                      t[1]] = dt.strftime('%Y-%m-%d %H:%M')
                post_dict['agenda_items-'+str(i)+'-value-description'] = \
                    doc['agenda'][i].get('desc', u'')
                post_dict['agenda_items-'+str(i)+'-value-location'] = \
                    doc['agenda'][i].get('location', u'')
                post_dict['agenda_items-'+str(i)+'-value-speakers-count'] = \
                    len(doc['agenda'][i].get('speakers', u''))
                if doc['agenda'][i].get('speakers'):
                    for y in range(len(doc['agenda'][i].get('speakers', u''))):
                        post_dict['agenda_items-'+str(i)+'-value-speakers-' +
                                  str(y)+'-value-name'] = \
                            doc['agenda'][i]['speakers'][y].get('name', u'')
                        post_dict['agenda_items-'+str(i)+'-value-speakers-' +
                                  str(y)+'-value-url'] = \
                            doc['agenda'][i]['speakers'][y].get('url', u'')
                        post_dict['agenda_items-'+str(i)+'-value-speakers-' +
                                  str(y)+'-order'] = y
                        post_dict['agenda_items-'+str(i)+'-value-speakers-' +
                                  str(y)+'-deleted'] = u''
        return post_dict
