Feature: Verify Prepaid product agreements database landing page works according to requirements
  As a first time visitor to the Prepaid product agreements database landing page
  I want to search prepaid product agreements by issuer name, product name, product type
  So that I can find the product information I'm looking for

@prepaid
Scenario Outline: Search prepaid product agreements by issuer name, product name, product type
  Given I visit the consumerfinance data-research/prepaid-accounts/search-agreements URL
  When I enter search term visa
  And I click on the "Search" product terms button
  Then I enter card issuer name <name>
  Then I check prepaid agreements for product <type>
  And I click on the "Apply filters" button
  Then I should find the text "<name>" on the page
  And I should find the text "<type>" on the page
Examples:
| name                                  | type                             |
| MetaBank                              | GPR (General Purpose Reloadable) |
| Sunrise Banks, National Association   | Other                            |
| MetaBank                              | Travel                           |
| BANCO POPULAR DE PUERTO RICO          | Payroll                          |
| Green Dot Bank                        | Digital wallet/P2P               |
| Google Payment Corp                   | Digital wallet/P2P               |
| PayPal                                | Digital wallet/P2P               |
| Comerica                              | Government benefits              |
| Comerica                              | Prison release                   |
| Sunrise Banks, National Association   | Refunds                          |
| Christian Community Credit Union      | Student                          |
| MetaBank                              | Tax                              |
