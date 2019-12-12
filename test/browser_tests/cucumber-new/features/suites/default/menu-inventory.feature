Feature: Inventory of all consumerfinance.gov pages
  As a public visitor to the consumerfinance.gov site
  I want to use the menu on the homepage
  So that I can navigate and view the content listed on the menu

# These flap inexplicably. Timeouts. Element not attached to page document.
@smoke_testing
Scenario Outline: Validate the submenu from a wagtail page and a django page
  Given I visit the www.consumerfinance.gov homepage
  When I use the "<menu_item>" menu to access "<sub_menu_link>"
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
  And I should see the page title as either "<key_text> > Consumer Financial Protection Bureau" or "<alt_key_text>"
  And I should see the last breadcrumb as case-insensitive "<key_text>"
  # Start from a Django page
  Given I visit the "www.consumerfinance.gov/jobs/" URL
  When I use the "<menu_item>" menu to access "<sub_menu_link>"
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
  And I should see the page title as either "<key_text> > Consumer Financial Protection Bureau" or "<alt_key_text>"
  And I should see the last breadcrumb as case-insensitive "<key_text>"

Examples:
| menu_item        | sub_menu_link                             | page_url                            | key_text                                                  | alt_key_text                      |
#| INSIDE THE CFPB  | About us                                  | the-bureau/                         | About us                                                  |                                   |
| INSIDE THE CFPB  | Jobs                                      | jobs/                               | Jobs                                                      |                                   |
| INSIDE THE CFPB  | Contact us                                | contact-us/                         | Contact us                                                |                                   |
| INSIDE THE CFPB  | Newsroom                                  | newsroom/                           | Newsroom                                                  |                                   |
| INSIDE THE CFPB  | Budget and performance                    | budget/                             | The CFPB budget                                           |                                   |
| INSIDE THE CFPB  | Blog                                      | blog/                               | Blog                                                      |                                   |
| INSIDE THE CFPB  | Advisory groups                           | advisory-groups/                    | Advisory groups                                           |                                   |
| INSIDE THE CFPB  | Doing business with us                    | doing-business-with-us/             | Doing business with us                                    |                                   |
| INSIDE THE CFPB  | Reports                                   | reports/                            | Reports                                                   | Reports Archive                   |
| GET ASSISTANCE   | Ask CFPB                                  | askcfpb/                            | Ask CFPB                                                  |                                   |
| GET ASSISTANCE   | Trouble paying your mortgage?             | mortgagehelp/                       | Mortgage help                                             |                                   |
| GET ASSISTANCE   | Protections against credit discrimination | fair-lending/                       | What protections do I have against credit discrimination? |                                   |
| GET ASSISTANCE   | Students                                  | students/                           | Students and young Americans                              |                                   |
| GET ASSISTANCE   | Older Americans                           | older-americans/                    | Financial protection for older Americans                  |                                   |
| GET ASSISTANCE   | Servicemembers and Veterans               | servicemembers/                     | Information for servicemembers                            |                                   |
| GET ASSISTANCE   | Community Banks & Credit Unions           | small-financial-services-providers/ | Community banks and credit unions                         |                                   |
| PARTICIPATE      | Credit cards                              | credit-cards/knowbeforeyouowe/      | Know Before You Owe                                       | Know Before You Owe: Credit Cards |
| PARTICIPATE      | Student loans                             | students/knowbeforeyouowe/          | Know Before You Owe: Student loans project                |                                   |
| PARTICIPATE      | Open government                           | open/                               | Open government                                           |                                   |
| PARTICIPATE      | Leadership calendar                       | leadership-calendar/                | Leadership Calendar                                       |                                   |
| PARTICIPATE      | FOIA                                      | foia/                               | Freedom of Information Act                                |                                   |
| PARTICIPATE      | Notice and comment                        | notice-and-comment/                 | Notice & Comment                                          |                                   |
| LAW & REGULATION | Guidance                                  | guidance/                           | Guidance documents                                        |                                   |
| LAW & REGULATION | Notice and comment                        | notice-and-comment/                 | Notice & Comment                                          |                                   |
| LAW & REGULATION | Regulations                               | regulations/                        | Regulations                                               |                                   |
| LAW & REGULATION | Amicus program                            | amicus/                             | Amicus program                                            |                                   |
| LAW & REGULATION | Administrative adjudication               | administrativeadjudication/         | Administrative adjudication                               |                                   |

@smoke_testing @wagtail
Scenario Outline: Validate the submenu from a wagtail page for pages without breadcrumbs
  Given I visit the www.consumerfinance.gov homepage
  When I use the "<menu_item>" menu to access "<sub_menu_link>"
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
  And I should see the page title as either "<key_text> > Consumer Financial Protection Bureau" or "<alt_key_text>"

Examples:
| menu_item          | sub_menu_link           | page_url                     | key_text                                                               | alt_key_text                                            |
| INSIDE THE CFPB    | Strategic plan          | strategic-plan/              | Consumer Financial Protection Bureau Strategic Plan FY 2013 - FY 2017  |                                                         |
| SUBMIT A COMPLAINT | Submit a complaint      | complaint/                   | Submit a complaint                                                     |                                                         |
| GET ASSISTANCE     | Paying for College      | paying-for-college/          | Paying for College                                                     |                                                         |
# the supervision manual screen does have a breadcrumb, but it's causing unicode errors
| LAW & REGULATION   | Examination manual      | guidance/supervision/manual/ | Supervision and Examination Manual                                     | Supervision and Examination Manual                      |
| GET ASSISTANCE     | Owning a Home           | owning-a-home/               | Owning a Home                                                          |                                                         |
| PARTICIPATE        | Tell Your Story         | your-story/                  | Your financial stories                                                 |                                                         |
| PARTICIPATE        | Mortgages               | know-before-you-owe/         | Know before you owe: Mortgages                                         |                                                         |
| GET ASSISTANCE     | Planning for Retirement | retirement/before-you-claim/ | Before You Claim                                                       |                                                         |
| PARTICIPATE        | Consumer Complaint Database | complaintdatabase/       | Consumer Complaint Database                               |                                   |

@smoke_testing @wagtail
Scenario Outline: Validate the submenu from a wagtail page for pages without breadcrumbs and without 'CFPB' in the page title
  Given I visit the www.consumerfinance.gov homepage
  When I use the "<menu_item>" menu to access "<sub_menu_link>"
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
    And I should see the page title contains "<key_text>"

Examples:
| menu_item   | sub_menu_link                         | page_url | key_text                         |
| PARTICIPATE | Home Mortgage Disclosure Act Database | hmda/    | The Home Mortgage Disclosure Act |
