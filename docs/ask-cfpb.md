# Ask CFPB API

This API provides search access to the English and Spanish content behind [Ask CFPB](https://www.consumerfinance.gov/ask-cfpb/) and [Obtener respuestas](https://www.consumerfinance.gov/es/obtener-respuestas/).

The financial topics covered include:

- Auto loans
- Bank accounts and services
- Credit cards
- Credit reports and scores
- Debt collection
- Families and money
- Money transfers
- Mortgages
- Payday loans
- Prepaid cards
- Student loans

## `Usage`
The API is a read-only resource that delivers search results in [json](https://www.json.org/) format.

Requests follow this pattern:

- `https://www.consumerfinance.gov/ask-cfpb/search/json/?q=[SEARCH TERMS]`

The json response will includes a list of results, each with a question, an answer, and a URL for the related CFPB page.
If no results are found, the "suggestion" field will offer a more promising search term if one can be found.


The payload for the search term "tuition" would look like this, but with more result entries:

```json
{
  query: "tuition",
  suggestion: null,
  result_query: "tuition",
  results: [
    {
      url: "https://www.consumerfinance.gov/ask-cfpb/what-is-a-tuition-payment-plan-en-563/",
      text: "Tuition payment plans, also called tuition installment plans, are short-term (12 months or less) payment plans that split your college bills into equal monthly payments. Tuition installment plans can be an alternative to student loans if you can afford to pay tuition, just not in a lump sum at the start of the semester or quarter. These payment plans do not generally charge interest, but they may have up-front fees. What is a tuition payment plan?",
      question: "What is a tuition payment plan?"
    }
  ]
}
```

## Spanish content

For questions and answers in Spanish, requests should follow this pattern:

- `https://www.consumerfinance.gov/es/obtener-respuestas/buscar/json/?q=[SPANISH SEARCH TERMS]`

The payload for the Spanish search term "vehiculo" would look like this, but with more result entries:

```json
{
  query: "vehiculo",
  suggestion: null,
  result_query: "vehiculo",
  results: [
    {
      url: "https://www.consumerfinance.gov/es/obtener-respuestas/como-puedo-averiguar-el-significado-de-los-terminos-de-mi-contrato-de-leasing-es-2047/",
      text: " Bajo la Ley de Arrendamientos del Consumidor (CLA, por sus siglas en inglés), la persona o compañía de quien usted hace el leasing de un vehículo, conocida como el "arrendador", deberá informar por escrito ciertos costos y plazos si el leasing es de más de cuatro meses y si cumple con otros requisitos. La mayoría de los arrendamientos de vehículos está sujeta a la CLA. Los siguientes materiales le pueden ayudar a entender los términos de su contrato de leasing. En el sitio web Comprenda cómo funciona la financiación de vehículos de la Comisión Federal de Comercio se ofrece la siguiente información en español: Antes de comprar un vehículo o hacer un leasing ¿Debería hacer un leasing para un vehículo? Glosario de términos específicos Más información en español de GobiernoUSA.gov: Consejos para comprar un auto usado: Arrendamiento con derecho a compra o “leasing”     Bajo la Ley de Arrendamientos del Consumidor (CLA, por sus siglas en ingles), la persona o compania de quien usted hace el leasing de un vehiculo, conocida como el "arrendador", debera informar por escrito ciertos costos y plazos si el leasing es de mas de cuatro meses y si cumple con otros requisitos. La mayoria de los arrendamientos de vehiculos esta sujeta a la CLA. Los siguientes materiales le pueden ayudar a entender los terminos de su contrato de leasing. En el sitio web Comprenda como funciona la financiacion de vehiculos de la Comision Federal de Comercio se ofrece la siguiente informacion en espanol: Antes de comprar un vehiculo o hacer un leasing Deberia hacer un leasing para un vehiculo? Glosario de terminos especificos Mas informacion en espanol de GobiernoUSA.gov: Consejos para comprar un auto usado: Arrendamiento con derecho a compra o leasing ¿Cómo puedo averiguar el significado de los términos de mi contrato de leasing? Como puedo averiguar el significado de los terminos de mi contrato de leasing?",
      question: "¿Cómo puedo averiguar el significado de los términos de mi contrato de leasing?"
    }
  ]
}
```
