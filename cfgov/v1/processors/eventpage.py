import datetime

import dateutil

from core.management.commands._helpers import PageDataConverter


class DataConverter(PageDataConverter):
    def format_tags(self, doc_tags):
        tags = ''
        for tag in doc_tags:
            if ' ' in tag:
                tag = '"%s"' % tag
            tags += tag + ', '
        if tags:
            tags = tags[0:-2]
        return tags

    def format_author(self, author):
        if not author or not author.get('name'):
            return u'""'
        return '"%s"' % author.get('name')

    def get_venue_dict(self, venue):
        venue_dict = {}
        if venue:
            if venue.get('name'):
                venue_dict['venue_name'] = venue['name']
            if venue.get('address'):
                for info in ['state', 'city', 'street', 'suite', 'zip']:
                    if venue['address'].get(info):
                        venue_dict['venue_'+info] = venue['address'][info]
        return venue_dict 

    def get_livestream_dict(self, livestream):
        livestream_dict = {}
        if livestream:
            for info in ['url', 'availability']:
                if livestream.get(info):
                    livestream_dict['live_stream_'+info] = livestream[info]
            if livestream.get('date') and livestream['date'].get('date'):
                dt = dateutil.parser.parse(livestream['date']['date'])
                livestream_dict['live_stream_date'] = dt.strftime('%Y-%m-%d')
        return livestream_dict

    def format_time_period_content(self, doc_tense, tense):
        # Time period content
        if not doc_tense or not doc_tense.get('summary'):
            return u''
        summary = doc_tense['summary']
        if 'http://content' in summary:
            summary = summary.replace('http://content', 'http://www')
        return summary

    def format_agenda_times(self, doc_agenda, t, index):
        if not doc_agenda[index] or not doc_agenda[index].get(t[0]):
            return u''
        if doc_agenda[index].get(t[0]).get('date'):
            time = doc_agenda[index][t[0]]['date']
            dt = dateutil.parser.parse(time)
            return dt.strftime('%Y-%m-%d %H:%M')

    def get_agenda_dict(self, doc_agenda):
        # Agenda
        agenda_dict = {}
        if not doc_agenda:
            agenda_dict['agenda_items-count'] = 0
            return agenda_dict
        agenda_dict['agenda_items-count'] = len(doc_agenda)
        for i in range(len(doc_agenda)):
            for info in (('order', i), ('type', 'item'), ('deleted', u'')):
                agenda_dict['agenda_items-'+str(i)+'-'+info[0]] = info[1]
            for t in [('beginning_time', 'start_dt'),('ending_time', 'end_dt')]:
                agenda_dict['agenda_items-'+str(i)+'-value-' + t[1]] = self.format_agenda_times(doc_agenda, t, i)

            agenda_dict['agenda_items-'+str(i)+'-value-description'] = doc_agenda[i].get('desc', u'')
            agenda_dict['agenda_items-'+str(i)+'-value-location'] = doc_agenda[i].get('location', u'')
            agenda_dict['agenda_items-'+str(i)+'-value-speakers-count'] = len(doc_agenda[i].get('speakers', u''))
            for y in range(len(doc_agenda[i].get('speakers', u''))):
                speakers_prefix = 'agenda_items-'+str(i)+'-value-speakers-' + str(y)
                agenda_dict[speakers_prefix+'-value-name'] = doc_agenda[i]['speakers'][y].get('name', u'')
                agenda_dict[speakers_prefix+'-value-url'] = doc_agenda[i]['speakers'][y].get('url', u'')
                agenda_dict[speakers_prefix+'-order'] = y
                agenda_dict[speakers_prefix+'-deleted'] = u''
        return agenda_dict

    def get_flickr_url(self, archive):
        if not archive or not archive.get('flickr'):
            return u''
        return archive['flickr']

    def get_youtube_url(self, archive):
        if not archive or not archive.get('youtube'):
            return u''
        return archive['youtube']

    def get_times_dict(self, beginning_time, ending_time):
        # Start and end times
        times_dict = {}
        times = [(beginning_time, 'start_dt'),
                 (ending_time, 'end_dt')]
        if times and times[0][0]:
            date = dateutil.parser.parse(times[0][0].get('date'))
            times_dict['date_published'] = date.strftime('%Y-%m-%d')
        else:
            times_dict['date_published'] = datetime.date.today()
        for t in times:
            if t[0]:
                dt = dateutil.parser.parse(t[0].get('date'))
                times_dict[t[1]] = dt.strftime('%Y-%m-%d %H:%M')
        return times_dict

    def convert(self, doc):
        post_dict = {
            'title':      doc.get('title', u''),
            'slug':       doc.get('slug', u''),
            'body':       doc.get('content', u''),
        }
        self.add_defaults(post_dict)

        post_dict['tags'] = self.format_tags(doc.get('tags'))
        post_dict['authors'] = self.format_author(doc.get('author'))
        post_dict['flickr_url'] = self.get_flickr_url(doc.get('archive'))
        post_dict['youtube_url'] = self.get_youtube_url(doc.get('archive'))
        post_dict.update(self.get_agenda_dict(doc.get('agenda')))
        post_dict.update(self.get_times_dict(doc.get('beginning_time'), doc.get('ending_time')))
        post_dict.update(self.get_livestream_dict(doc.get('live_stream')))
        post_dict.update(self.get_venue_dict(doc.get('venue')))
        for tense in ['archive', 'live', 'future']:
            post_dict[tense+'_body'] = self.format_time_period_content(doc.get(tense), tense)
        
        return post_dict
