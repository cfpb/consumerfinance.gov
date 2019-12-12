Feature: Submit a complaint and Consumer Complaint Database
  As a public visitor to consumerfinance.gov
  I want to view the complaint pages and navigate their links
  So that I Submit a complaint and learn about the complaint database

@smoke_testing @complaint @complaint_data_use
Scenario Outline: Reach the Monthly Complaint Reports from the How we use complaint data page
  Given I visit the "www.consumerfinance.gov/complaint/data-use" URL
  When I click on the "Volume <volume_number>" link
  Then I should be directed to the "www.consumerfinance.gov/data-research/research-reports/monthly-complaint-report-vol-<volume_number>/" URL
    And I should see the page title contains "Monthly Complaint Report, Vol. <volume_number>"
    And I should find the text "Research & Reports" on the page

Examples:
| volume_number |
| 10 |
| 9 |
| 8 |
| 7 |
| 6 |
| 5 |
| 4 |
| 3 |
| 2 |
| 1 |

@smoke_testing @complaint @complaint_data_use
Scenario Outline: Reach the Reports pages from the How we use complaint data page
  Given I visit the "www.consumerfinance.gov/complaint/data-use" URL
  When I click on the report link "<report_link_text>" for "<report_year>" under "<report_type>"
  Then I should be directed to the "www.consumerfinance.gov/data-research/research-reports/<report_slug>/" URL
    And I should see the page title contains "<report_title>"
    And I should find the text "Research & Reports" on the page

Examples:
| report_type | report_year | report_link_text | report_slug | report_title |
| Reports to Congress | 2018 | Annual report | 2018-consumer-response-annual-report | 2018 Consumer Response Annual Report |
| Reports to Congress | 2017 | Annual report | 2017-consumer-response-annual-report | 2017 Consumer Response Annual Report |
| Reports to Congress | 2016 | Annual report | 2016-consumer-response-annual-report | 2016 Consumer Response Annual Report |
| Reports to Congress | 2015 | Annual report | 2015-consumer-response-annual-report | 2015 Consumer Response Annual Report |
| Reports to Congress | 2014 | Annual report | 2014-consumer-response-annual-report | 2014 Consumer Response Annual Report |
| Reports to Congress | 2014 | Semi-annual report | semi-annual-report-spring-2014 | Semi-Annual Report Spring 2014 |
| Reports to Congress | 2013 | Annual report | 2013-consumer-response-annual-report | 2013 Consumer Response annual report |
| Reports to Congress | 2012 | Annual report | consumer-response-annual-report-2012 | 2012 Consumer Response annual report |
| Reports to Congress | 2012 | Semi-annual report | semi-annual-report-2 | Semi-Annual Report |
| Reports to Congress | 2011 | Annual report | consumer-response-annual-report | Consumer Response Annual Report |
| Reports to Congress | 2011 | Semi-annual report | semi-annual-report-of-the-consumer-financial-protection-bureau | Semi-Annual Report of the Consumer Financial Protection Bureau |
| Reports to Congress | 2011 | Consumer Response interim report on CFPB's credit card complaint data | consumer-response-interim-report-cfpbs-credit-card-complaint-data | Consumer Response interim report on CFPB's credit card complaint data |
| Snapshots of complaints received | 2013 | July report | a-snapshot-of-complaints-received-3 | A Snapshot of Complaints Received |

@smoke_testing @complaint @complaint_data_use
Scenario Outline: Reach PDF Reports from the How we use complaint data page
  Given I visit the "www.consumerfinance.gov/complaint/data-use" URL
  When I click on the report link "<pdf_report_link_text>" for "<pdf_report_year>" under "<pdf_report_type>"
  Then I should be directed to the external "<pdf_report_url>" URL

Examples:
| pdf_report_type | pdf_report_year | pdf_report_link_text | pdf_report_url |
| Complaints by the numbers | 2015 | 2015 report | http://files.consumerfinance.gov/f/201503_cfpb_complaints-by-the-numbers.pdf |
| Snapshots of complaints received | 2014 | July report | http://files.consumerfinance.gov/f/201407_cfpb_report_consumer-complaint-snapshot.pdf |
| Snapshots of complaints received | 2013 | March report | http://files.consumerfinance.gov/f/201303_cfpb_Snapshot-March-2013.pdf |
| Snapshots of complaints received | 2012 | June report | http://files.consumerfinance.gov/f/201206_cfpb_shapshot_complaints-received.pdf |
