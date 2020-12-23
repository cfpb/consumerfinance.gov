Feature: Verify regulations search page works according to requirements
  As a first time visitor to the regulations search page
  I want to Search regulations on the page
  So that I can find the information I'm looking for

@reg_search
Scenario Outline: Search regulations
  Given I visit the consumerfinance policy-compliance/rulemaking/regulations/search-regulations/results/?regs=<reg> URL
  When I Enter Search regulations term manually <search_term>
  And I click on the "Search" regulation button
  Then I should find the text "<search_term>" on the page
Examples:
| reg  | search_term  |
| 1002 | finance      |
| 1003 | finance      |
| 1004 | finance      |
| 1005 | payroll card |
| 1007 | mortgage     |
| 1008 | finance      |
| 1010 | mortgage     |
| 1011 | land         |
| 1012 | registration |
| 1013 | registration |
| 1016 | mortgage     |
| 1022 | finance      |
| 1024 | finance      |
| 1026 | finance      |
| 1030 | savings      |
| 1041 | payroll card |
