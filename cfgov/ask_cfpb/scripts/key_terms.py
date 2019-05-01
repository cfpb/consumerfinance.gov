# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from bs4 import BeautifulSoup as bs
import HTMLParser

from v1.models import CFGOVPage
from v1.models.snippets import GlossaryTerm
from v1.models import PortalTopic

portals = {
    'auto-loans': 'Auto loans',
    'credit-reports-and-scores': 'Credit reports and scores',
    'debt-collection': 'Debt collection',
    'mortgages': 'Mortgages',
    'fraud': 'Fraud and scams',
    'student-loans': 'Student loans',
    'bank-accounts': 'Bank accounts',
    'prepaid-cards': 'Prepaid cards'
}


def run():
    for term in GlossaryTerm.objects.all():
        term.delete() 
    keys = portals.keys()
    for page in CFGOVPage.objects.filter(slug='key-terms'):
        parent_slug = page.get_parent().slug
        if parent_slug in keys:
            portal_topic = PortalTopic.objects.filter(heading=portals[parent_slug])[0]
            for block in page.specific.content:
                if block.block_type == 'full_width_text':
                    for child in block.value:
                        if child.block_type == 'content':
                            contents = bs(child.value.source, 'html.parser')
                            headings = contents.findAll('h3')
                            for h3 in headings:
                                if h3.text:
                                    h3_contents = bs(h3.contents[0], 'html.parser')
                                    div = h3_contents.find('div')
                                    anchor = div.get('id')
                                    term = div.text
                                    definition = ''
                                    sibling = h3.next_sibling
                                    while sibling and sibling.name != 'h3':
                                        if sibling.text:
                                            definition += sibling.encode(formatter="html")
                                        sibling = sibling.next_sibling
                                    glossary_term = GlossaryTerm(
                                        term=term,
                                        definition=definition,
                                        anchor=anchor,
                                        portal_topic=portal_topic
                                    )
                                    glossary_term.save()

                                    
                                    


