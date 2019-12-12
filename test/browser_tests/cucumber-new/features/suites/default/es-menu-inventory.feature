Feature: Inventory of all consumerfinance.gov Spanish language pages
  As a public visitor to the consumerfinance.gov/es site
  I want to use the menu on the homepage
  So that I can navigate and view the Spanish language content listed on the menu

@smoke_testing @spanish_language @spanish_titles
Scenario Outline: Reach the Spanish language page through the menu
  Given I visit the www.consumerfinance.gov/es homepage
  When I click on the "<menu_item>" item
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
    And I should see the page title as "<key_text> > Oficina para la Protección Financiera del Consumidor"
    And I should find the text "<body_text>" on the page

Examples:
| menu_item           | page_url                | key_text                                             | body_text                                                 |
| OBTENER RESPUESTAS  | es/obtener-respuestas/  | Obtener Respuestas                                   | Encontrar respuestas a preguntas                          |
| PRESENTAR UNA QUEJA | es/presentar-una-queja/ | Después de presentar una queja                       | Usted presenta una queja sobre                            |
| QUIENES SOMOS       | es/quienes-somos/       | ¿Quiénes somos?                                      | Entre otras cosas, nosotros                               |
| HOGAR               | es/hogar/               | Hogar                                                | ¿Le gustaría comprar una casa?                            |

@spanish_language @spanish_logo
Scenario Outline: click on the Spanish language CFPB logo image through the menu
  Given I visit the www.consumerfinance.gov/es<page_url> URL
  When I click on the Spanish language CFPB logo image
  Then I should be directed to the "www.consumerfinance.gov/es/" URL
    And I should see the page title as "Oficina para la Protección Financiera del Consumidor > Oficina para la Protección Financiera del Consumidor"
    And I should see the Facebook iFrame
    And I should find the text "¿Tiene problemas con un producto o servicio financiero?" on the page

Examples:
| page_url              |
| /obtener-respuestas/  |
| /presentar-una-queja/ |
| /quienes-somos/       |
| /hogar/               |

# These fail inconsistently but frequently
@spanish_language @spanish_titles @flapper
Scenario Outline: Reach the Spanish language page through the menu
  Given I visit the www.consumerfinance.gov/es homepage
  When I click on the "<menu_item>" item
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
    And I should see the page title as "<key_text> > Oficina para la Protección Financiera del Consumidor"
    And I should find the text "<body_text>" on the page

Examples:
| menu_item | page_url | key_text                                             | body_text                                               |
| INICIO    | es/      | Oficina para la Protección Financiera del Consumidor | ¿Tiene problemas con un producto o servicio financiero? |
