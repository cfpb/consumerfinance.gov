Feature: Test the Ask CFPB page in English and Spanish
  As a public visitor to the consumerfinance.gov site
  I want to search using the Ask CFPB page in English and Spanish
  So that I can verify the correct results are returned

@smoke_testing @ask_cfpb 
Scenario Outline: Make sure incorrect slug in URL is corrected
  Given I visit the incorrect "www.consumerfinance.gov/<bad_url>" URL
  Then I should be directed to "www.consumerfinance.gov/<correct_url>" URL
  And I should see the page title contains "<title>"

Examples:
| bad_url                                           | correct_url                           | title                    |
| ask-cfpb/1163/what-wire-transfer_THIS_IS_Bad.html | ask-cfpb/1163/what-wire-transfer.html | What is a wire transfer? |
| ask-cfpb/1065/what-is-an-ach_THIS_IS_BAD.html     | ask-cfpb/1065/what-is-an-ach.html     | What is an ACH?          |
| es/obtener-respuestas/c/manejar-una-cuenta-bancaria/983/como-suspendo-el-pago-de-un-cheque_BAD.html | es/obtener-respuestas/c/manejar-una-cuenta-bancaria/983/como-suspendo-el-pago-de-un-cheque.html | ¿Cómo suspendo el pago de un cheque? |
| es/obtener-respuestas/c/obtener-una-tarjeta-de-credito/47/que-es-un-periodo_BAD.html                | es/obtener-respuestas/c/obtener-una-tarjeta-de-credito/47/que-es-un-periodo-de-gracia-como-funciona.html | Qué es un período de gracia |

@smoke_testing @ask_cfpb
Scenario Outline: In Ask CFPB, verify that the search button becomes enabled after typing at least one character
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  When I enter "<search_text>" in the ask cfpb search box
  Then I should see the search button is "enabled"

Examples:
| page_url               | search_text |
| ask-cfpb/              | money       |
#| es/obtener-respuestas/ | dinero      |

@ask_cfpb_autocomplete
Scenario Outline: Search for a term, select a question using auto-complete and verify that the window title includes the search term
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  When I select what I call the "search" text box and search "<search_text>" and choose "<link_text>"
  Then I should see the page title contains "<link_text>"

Examples:
| page_url               | search_text | link_text                                    |
| ask-cfpb/              | money       | Is a money market account insured?           |
| ask-cfpb/              | credit      | What is credit counseling?                   |
| ask-cfpb/              | loan        | What is a Stafford loan?                     |
| es/obtener-respuestas/ | dinero      | ¿Puedo cancelar una transferencia de dinero? |
| es/obtener-respuestas/ | credito     | ¿Quién tiene un informe de crédito?          |
| es/obtener-respuestas/ | prestamo    | ¿Qué es un préstamo PLUS?                    |

@ask_cfpb
Scenario Outline: Search for a term, with NO auto-complete and verify that the window title includes the search term
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  When I enter "<search_text>" in the "q" text box
  Then I should see the page title contains "<title_text> '<search_text>'"

Examples:
| page_url               | title_text         | search_text |
| ask-cfpb/              | Search Results for | money       |
| ask-cfpb/              | Search Results for | credit      |
| es/obtener-respuestas/ | Buscar por         | dinero      |
| es/obtener-respuestas/ | Buscar por         | credito     |

@ask_cfpb
Scenario: Search the Ask CFPB page for 'reverse' and reach the 'What is a reverse mortgage?' page
  Given I visit the www.consumerfinance.gov/askcfpb/ URL
  When I select what I call the "search" text box and search "reverse" and choose "What is a reverse mortgage?"
  Then I should be directed to the "www.consumerfinance.gov/askcfpb/224/what-is-a-reverse-mortgage.html" URL
  And I should see the page title contains "What is a reverse mortgage"
  And I should see the last breadcrumb as "WHAT IS A REVERSE MORTGAGE?"
  And I should find the text "What is a reverse mortgage?" on the page

@security @ask_cfpb @spanish_language
Scenario Outline: Search the Obtener Respuestas page and have Spanish unicode characters url-encoded
  Given I visit the "www.consumerfinance.gov/es/obtener-respuestas/" URL
  When I enter "<search_term>" in the "q" text box
  Then I should see results at the "www.consumerfinance.gov/es/obtener-respuestas/buscar?<query_param>" URL
  And I should see the page title contains "Buscar por"
  And I should find the text "Encontrar respuestas a preguntas" on the page

Examples:
| search_term   | query_param                                              |
| á             | q=%C3%A1                                                 |
| é             | q=%C3%A9                                                 |
| í             | q=%C3%AD                                                 |
| áéíóúüñ¿¡     | q=%C3%A1%C3%A9%C3%AD%C3%B3%C3%BA%C3%BC%C3%B1%C2%BF%C2%A1 |
| ¿Comocrédito? | q=%C2%BFComocr%C3%A9dito%3F                              |
# 精神相對待
# note: due to a bug in chromedriver on linux, we can't use spaces in the search strings above
