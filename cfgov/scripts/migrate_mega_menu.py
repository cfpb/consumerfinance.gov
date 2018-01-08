from wagtail.wagtailcore.blocks import StreamValue

from v1.models.snippets import MenuItem

menu_items = [  
    {  
        'link_text':'Consumer Tools',
        'external_link':'#',
        'order': 1,
        'featured_content':{  
            'type':'featured_content',
            'value':{  
                'link':{  
                    'text':'Get your financial well-being score',
                    'url':'/consumer-tools/financial-well-being/',

                },
                'image':{  
                    'url':'img/fmc-consumer-tools-540x300.png',
                    'alt':'',

                },
                'body':'Answer ten questions and see your financial well-being score, ' + 
                       'along with national averages.',
            }
        },
        'footer':{  
            'type':'footer',
            'value': {
                'content': '<p>Browse answers to hundreds of financial questions. <a href="/ask-cfpb/" class="o-mega-menu_content-link">Ask CFPB</a></p><p>Have an issue with a financial product? <a href="/complaint/" class="o-mega-menu_content-link">Submit a complaint</a></p>'
            },
        },
        'nav_groups':[  
            {  
                'type':'nav_group',
                'value':{  
                    'group_title':'Money Topics',
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Auto Loans',
                                'external_link':'/consumer-tools/auto-loans/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Bank Accounts & Services',
                                'external_link':'/consumer-tools/bank-accounts/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Credit Cards',
                                'external_link':'/ask-cfpb/category-credit-cards/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Credit Reports & Scores',
                                'external_link':'/consumer-tools/credit-reports-and-scores/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Debt Collection',
                                'external_link':'/consumer-tools/debt-collection/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'group_title':'Money Topics',
                    'hide_group_title':'true',
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Money Transfers',
                                'external_link':'/sending-money/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Mortgages',
                                'external_link':'/consumer-tools/mortgages/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Payday Loans',
                                'external_link':'/ask-cfpb/category-payday-loans/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Prepaid Cards',
                                'external_link':'/consumer-tools/prepaid-cards/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Student Loans',
                                'external_link':'/consumer-tools/student-loans/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'group_title':'Guides',
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Getting an Auto Loan',
                                'external_link':'/consumer-tools/getting-an-auto-loan/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Managing Someone Else\'s Money',
                                'external_link':'/consumer-tools/managing-someone-elses-money/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Money as You Grow',
                                'external_link':'/consumer-tools/money-as-you-grow/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Navigating the Military Financial Lifecycle',
                                'external_link':'/consumer-tools/military-financial-lifecycle/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Owning a Home',
                                'external_link':'/owning-a-home/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Paying for College',
                                'external_link':'/paying-for-college/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Planning for Retirement',
                                'external_link':'/consumer-tools/retirement/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },

        ],

    },
    {  
        'link_text':'Practitioner Resources',
        'external_link':'#',
        'order': 2,
        'featured_content':{  
            'type':'featured_content',
            'value':{  
                'link':{  
                    'text':'Explore financial well-being survey results',
                    'url':'/data-research/research-reports/financial-well-being-america/',

                },
                'image':{  
                    'url':'img/fmc-resources-540x300.png',
                    'alt':'',

                },
                'body':'See national survey results on financial well-being and how it '                + 
                        'relates to other factors in a person\'s financial life.',

            }
        },
        'footer':{  
            'type':'footer',
            'value': {
                'content': '<p><a href="https://pueblo.gpo.gov/CFPBPubs/CFPBPubs.php" class="o-mega-menu_content-link">Order free brochures</a></p>'
            }
        },
        'nav_groups':[  
            {  
                'type':'nav_group',
                'value':{  
                    'group_title':'Populations Served',
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Adult Financial Education',
                                'external_link':'/practitioner-resources/adult-financial-education/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Economically Vulnerable Consumers',
                                'external_link':'/practitioner-resources/economically-vulnerable/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Older Adults & Their Families',
                                'external_link':'/practitioner-resources/resources-for-older-adults/'
                            },
                            'nav_items':[]
                        }
                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'group_title':'Populations Served',
                    'hide_group_title':'true',
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Servicemembers & Veterans',
                                'external_link':'/practitioner-resources/servicemembers/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Students & Student Loan Borrowers',
                                'external_link':'/practitioner-resources/students/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Youth Financial Education',
                                'external_link':'/practitioner-resources/youth-financial-education/'
                            },
                            'nav_items':[]
                        }
                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'group_title':'Programs',
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Resources for Libraries',
                                'external_link':'/practitioner-resources/library-resources/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Resources for Tax Preparers',
                                'external_link':'/practitioner-resources/resources-for-tax-preparers/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Your Money, Your Goals',
                                'external_link':'/practitioner-resources/your-money-your-goals/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },

        ],

    },
    {  
        'link_text':'Data & Research',
        'external_link':'/data-research/',
        'order': 3,
        'featured_content':{  
            'type':'featured_content',
            'value':{  
                'link':{  
                    'text':'Help advance financial well-being',
                    'url':'/data-research/financial-well-being-survey-data/',

                },
                'image':{  
                    'url':'img/fmc-data-research-540x300.png',
                    'alt':'',

                },
                'body':'Explore our national survey data and think about ways to empower '                + 
                        'families to achieve higher financial well-being.',

            }
        },
        'nav_groups':[  
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Research & Reports',
                                'external_link':'/data-research/research-reports/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Consumer Complaint Database',
                                'external_link':'/data-research/consumer-complaints/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Mortgage Database (HMDA)',
                                'external_link':'/data-research/mortgage-data-hmda/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Consumer Credit Trends',
                                'external_link':'/data-research/consumer-credit-trends/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Mortgage Performance Trends',
                                'external_link':'/data-research/mortgage-performance-trends/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Financial Well-Being Survey',
                                'external_link':'/data-research/financial-well-being-survey-data/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Credit Card Surveys & Agreements',
                                'external_link':'/data-research/credit-card-data/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'CFPB Research Conference',
                                'external_link':'/data-research/cfpb-research-conference/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'CFPB Researchers',
                                'external_link':'/data-research/cfpb-researchers/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            }
        ],

    },
    {  
        'link_text':'Policy & Compliance',
        'external_link':'/policy-compliance/',
        'order': 4,
        'featured_content':{  
            'type':'featured_content',
            'value':{  
                'link':{  
                    'text':'Resources to help you comply',
                    'url':'/policy-compliance/guidance/implementation-guidance/',

                },
                'image':{  
                    'url':'img/fmc-poly-com-540x300.jpg',
                    'alt':'',

                },
                'body':'The TILA-RESPA integrated disclosure rule '                + 
                        'replaces four disclosure forms with two new ones. ' + 
                        'We have resources to help you comply.',

            }
        },
        'nav_groups':[  
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Rulemaking',
                                'external_link':'/policy-compliance/rulemaking/',
                            },
                            'nav_items':[  
                                {  
                                    'link':{  
                                        'link_text':'Final Rules',
                                        'external_link':'/policy-compliance/rulemaking/final-rules/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Rules Under Development',
                                        'external_link':'/policy-compliance/rulemaking/rules-under-development/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Regulatory Agenda',
                                        'external_link':'/policy-compliance/rulemaking/regulatory-agenda/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Small Business Review Panels',
                                        'external_link':'/policy-compliance/rulemaking/small-business-review-panels/'
                                    }
                                },

                            ]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Compliance & Guidance',
                                'external_link':'/policy-compliance/guidance/'
                            },
                            'nav_items':[  
                                {  
                                    'link':{  
                                        'link_text':'Implementation & Guidance',
                                        'external_link':'/policy-compliance/guidance/implementation-guidance/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Supervision & Examinations',
                                        'external_link':'/policy-compliance/guidance/supervision-examinations/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Supervisory Highlights',
                                        'external_link':'/policy-compliance/guidance/supervisory-highlights/'
                                    }
                                },

                            ]
                        },
                        {  
                            'link':{  
                                'link_text':'Enforcement',
                                'external_link':'/policy-compliance/enforcement/'
                            },
                            'nav_items':[  
                                {  
                                    'link':{  
                                        'link_text':'Enforcement Actions',
                                        'external_link':'/policy-compliance/enforcement/actions/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Petitions to Modify or Set Aside',
                                        'external_link':'/policy-compliance/enforcement/petitions/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Warning Letters',
                                        'external_link':'/policy-compliance/enforcement/warning-letters/'
                                    }
                                },

                            ]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Notices & Opportunities to Comment',
                                'external_link':'/policy-compliance/notice-opportunities-comment/',

                            },
                            'nav_items':[  
                                {  
                                    'link':{  
                                        'link_text':'Open Notices',
                                        'external_link':'/policy-compliance/notice-opportunities-comment/open-notices/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Archive of Closed Notices',
                                        'external_link':'/policy-compliance/notice-opportunities-comment/archive-closed/'
                                    }
                                },

                            ]
                        },
                        {  
                            'link':{  
                                'link_text':'Amicus Program',
                                'external_link':'/policy-compliance/amicus/',

                            },
                            'nav_items':[  
                                {  
                                    'link':{  
                                        'link_text':'Filed Briefs',
                                        'external_link':'/policy-compliance/amicus/briefs/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Suggest a Case',
                                        'external_link':'/policy-compliance/amicus/suggest/'
                                    }
                                },

                            ]
                        },

                    ]
                }
            },

        ],

    },
    {  
        'link_text':'About Us',
        'external_link':'/about-us/',
        'order': 5,
        'nav_groups':[  
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'The Bureau',
                                'external_link':'/about-us/the-bureau/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Budget & Strategy',
                                'external_link':'/about-us/budget-strategy/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Payments to Harmed Consumers',
                                'external_link':'/about-us/payments-harmed-consumers/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Recent Updates',
                                'external_link':'/activity-log/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Blog',
                                'external_link':'/about-us/blog/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Newsroom',
                                'external_link':'/about-us/newsroom/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Events',
                                'external_link':'/about-us/events/'
                            },
                            'nav_items':[]
                        },

                    ]
                }
            },
            {  
                'type':'nav_group',
                'value':{  
                    'nav_items':[  
                        {  
                            'link':{  
                                'link_text':'Careers',
                                'external_link':'/about-us/careers/',

                            },
                            'nav_items':[  
                                {  
                                    'link':{  
                                        'link_text':'Working @ CFPB',
                                        'external_link':'/about-us/careers/working-at-cfpb/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Job Application Process',
                                        'external_link':'/about-us/careers/application-process/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'Students & Recent Graduates',
                                        'external_link':'/about-us/careers/students-and-graduates/'
                                    }
                                },
                                {  
                                    'link':{  
                                        'link_text':'All Current Openings',
                                        'external_link':'/about-us/careers/current-openings/'
                                    }
                                },

                            ]
                        },
                        {  
                            'link':{  
                                'link_text':'Doing Business With Us',
                                'external_link':'/about-us/doing-business-with-us/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Advisory Groups',
                                'external_link':'/about-us/advisory-groups/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Project Catalyst',
                                'external_link':'/about-us/project-catalyst/'
                            },
                            'nav_items':[]
                        },
                        {  
                            'link':{  
                                'link_text':'Contact Us',
                                'external_link':'/about-us/contact-us/'
                            },
                            'nav_items':[]
                        },
                    ]
                }
            },
        ],
    },
]


def migrate_menu():
    MenuItem.objects.all().delete()
    for item in menu_items:  
        menu_item = MenuItem(
            link_text=item['link_text'],
            external_link=str(item['external_link']),
            order=item['order'],
        )
        for i, group in enumerate(item['nav_groups']):
            column_block = getattr(menu_item, 'column_{}'.format(i + 1))
            stream_block = getattr(column_block, 'stream_block')
            setattr(menu_item, 'column_{}'.format(i + 1), StreamValue(
                stream_block,
                [group],
                True,
            ))
        if item.get('footer'):
            menu_item.footer = StreamValue(
                menu_item.footer.stream_block,
                [item['footer']],
                True,
            )
        if item.get('featured_content'):
            menu_item.column_4 = StreamValue(
                menu_item.column_4.stream_block,
                [item['featured_content']],
                True,
            )
        menu_item.save()


def run():
    migrate_menu()
