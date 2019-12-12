Feature: Submit a complaint and Consumer Complaint Database
  As a public visitor to consumerfinance.gov
  I want to view the complaint pages and navigate their links
  So that I Submit a complaint and learn about the complaint database

@smoke_testing @complaint @complaintforms
Scenario Outline: Find the correct Submit a complaint form for products with multiple complaint links
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the "<product_link_text>" link
  Then I should be directed to the "www.consumerfinance.gov/complaint/#<section_id>" URL
    When I click the input element with the "<input_id>" id
    Then I should find the text "<text>" on the page
    Then I should find the "Get started" link on the page
    When I click on the "Get started" link
    Then I should be directed to the external "<complaint_form_url>" URL
      And I should find the text "<form_heading>" on the page

Examples:
| product_link_text | section_id | input_id | text | complaint_form_url | form_heading |
| Student loan | student-loan | radio-student-loan-federal | Submit a federal student loan complaint to the CFPB | https://help.consumerfinance.gov/app/studentloan/ask | Submit a student loan complaint |
| Student loan | student-loan | radio-student-loan-private | Submit a private student loan complaint to the CFPB | https://help.consumerfinance.gov/app/studentloan/ask | Submit a student loan complaint |
| Credit card or prepaid card | credit-card | radio-credit-card |  Submit a credit card complaint to the CFPB | https://help.consumerfinance.gov/app/creditcard/ask | Submit a credit card complaint |
| Credit card or prepaid card | credit-card | radio-debit-card |  Submit a debit card complaint to the CFPB | https://help.consumerfinance.gov/app/bankaccountorservice/ask | Submit a bank account or service complaint |
| Money transfer or virtual currency | money-transfer | radio-money-transfer |  Submit a money transfer complaint to the CFPB | https://help.consumerfinance.gov/app/moneytransfers/ask | Submit a money transfer complaint |
| Money transfer or virtual currency | money-transfer | radio-virtual-currency |  We're developing a new virtual currency complaint form | https://help.consumerfinance.gov/app/moneytransfers/ask | Submit a money transfer complaint |
| Credit card or prepaid card | credit-card | radio-prepaid-card |  Submit a prepaid card complaint to the CFPB | https://help.consumerfinance.gov/app/prepaid/ask#currentPage=0 | Submit a prepaid card complaint |
| Other financial service | other-service | radio-check-cashing |  Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/258#currentPage=0 | Submit an other financial service complaint |
| Other financial service | other-service | radio-foreign-currency-exchange |  Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/1206#currentPage=0 | Submit an other financial service complaint |
| Other financial service | other-service | radio-money-order |  Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/3072#currentPage=0 | Submit an other financial service complaint |
| Other financial service | other-service | radio-refund-anticipation-check |  Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/250#currentPage=0 | Submit an other financial service complaint |
| Other financial service | other-service | radio-travelers-check |  Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/3073#currentPage=0 | Submit an other financial service complaint |

@smoke_testing @complaint @complaintforms
Scenario Outline: Find the correct Submit a complaint form for a specific type of complaint
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the "<product_link_text>" link
  Then I should be directed to the "www.consumerfinance.gov/complaint/#<section_id>" URL
    Then I should find the text "<text>" on the page
    Then I should find the "Get started" link on the page
    When I click on the "Get started" link
    Then I should be directed to the external "<complaint_form_url>" URL
      And I should find the text "<form_heading>" on the page

Examples:
| product_link_text | section_id | text | complaint_form_url | form_heading |
| Mortgage | mortgage | Submit a mortgage complaint to the CFPB | https://help.consumerfinance.gov/app/mortgage/ask | Submit a mortgage complaint |
| Vehicle loan or lease | vehicle | Submit a vehicle loan or lease complaint | https://help.consumerfinance.gov/app/vehicleconsumerloan/ask | Submit a vehicle loan or consumer loan complaint |
| Payday loan | payday-loan | Submit a payday loan complaint to the CFPB | https://help.consumerfinance.gov/app/payday/ask#currentPage=0 | Submit a payday or other consumer loan complaint |
| Other consumer loan | other-loan |  Submit an online, store, or other loan complaint to the CFPB | https://help.consumerfinance.gov/app/payday/ask#currentPage=0 | Submit a payday or other consumer loan complaint |
| Bank account or service | bank-account |  Submit a bank account or service complaint to the CFPB | https://help.consumerfinance.gov/app/bankaccountorservice/ask | Submit a bank account or service complaint |
| Credit reporting | credit-reporting |  Submit a credit reporting complaint to the CFPB | https://help.consumerfinance.gov/app/creditreporting/ask | Submit a credit reporting complaint |
| Debt collection | debt-collection |  Submit a debt collection complaint to the CFPB | https://help.consumerfinance.gov/app/debtcollection/ask#currentPage=0 | Submit a debt collection complaint |

@smoke_testing @complaint @complaintforms
Scenario Outline: Find the correct Submit a complaint form for credit report or debt settlement complaints
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the "<product_link_text>" link
  Then I should be directed to the "www.consumerfinance.gov/complaint/#<section_id>" URL
    When I click the input element with the "<input_id>" id
    Then I should find the text "Which of these best describes your issue?" on the page
    When I click the input element with the "<input_id_2>" id
    Then I should find the text "<text>" on the page
    Then I should find the "Get started" link on the page
    When I click on the "Get started" link
    Then I should be directed to the external "<complaint_form_url>" URL
      And I should find the text "<form_heading>" on the page

Examples:
| product_link_text | section_id | input_id | input_id_2 | text | complaint_form_url | form_heading |
| Other financial service | other-service | radio-credit-repair | radio2-credit-report |  Submit a credit reporting complaint to the CFPB | https://help.consumerfinance.gov/app/creditreporting/ask | Submit a credit reporting complaint |
| Other financial service | other-service | radio-credit-repair | radio2-credit-repair |  Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/3070#currentPage=0 | Submit an other financial service complaint |
| Other financial service | other-service | radio-debt-settlement | radio2-debt-collector |  Submit a debt collection complaint to the CFPB | https://help.consumerfinance.gov/app/debtcollection/ask#currentPage=0 | Submit a debt collection complaint |
| Other financial service | other-service | radio-debt-settlement | radio2-debt-settlement | Submit an other financial service complaint to the CFPB | https://help.consumerfinance.gov/app/other/ask/p_id/3071#currentPage=0 | Submit an other financial service complaint |

@smoke_testing @complaint @complaintlinks
Scenario: Reach the complaint status login page from the Submit a complaint page
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the "Check complaint status" link
  Then I should be directed to the external "https://help.consumerfinance.gov/app/utils/login_form/" URL
    And I should find the text "User Name" on the page
    And I should find the text "Password" on the page

@smoke_testing @complaint @complaintlinks
Scenario: Reach the complaint status login page from the Submit a complaint page
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the "First login?" link
  Then I should be directed to the external "https://help.consumerfinance.gov/app/utils/account_assistance" URL
    And I should find the text "Set your password" on the page

@smoke_testing @complaint @complaintlinks @complaintlearnmore
Scenario: Reach the complaint process page from the Submit a complaint page
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the Learn More link under "What happens after I submit a complaint?"
  Then I should be directed to the "www.consumerfinance.gov/complaint/process/" URL
    And I should see the page title as "The complaint process > Consumer Financial Protection Bureau"

@smoke_testing @complaint @complaintlinks @complaintlearnmore
Scenario: Reach the data use page from the Submit a complaint page
  Given I visit the "www.consumerfinance.gov/complaint" URL
  When I click on the Learn More link under "How will you use my information?"
  Then I should be directed to the "www.consumerfinance.gov/complaint/data-use/" URL
    And I should see the page title as "How we use complaint data > Consumer Financial Protection Bureau"
