# Site Search

Global site search of consumerfinance.gov is implemented using
[Search.gov](https://search.gov/).

The search box in the site header is linked to this global site search.
Searches using this method return results at the `search.consumerfinance.gov`
subdomain. This subdomain is hosted by Search.gov.

We maintain several independent search indexes on Search.gov for various purposes:

- `cfpb`: English-language search for
  [www.consumerfinance.gov](https://www.consumerfinance.gov).
- `cfpb_es`: Spanish-language search for pages under
  [www.consumerfinance.gov/es/](https://www.consumerfinance.gov/es/).
- `cfpb_beta`: An alternate English-language search index for
  [beta.consumerfinance.gov](https://beta.consumerfinance.gov).
- `cfpb_beta_es`: An alternate Spanish-language search index for
  [beta.consumerfinance.gov/es/](https://beta.consumerfinance.gov/es/).

These search indexes are hardcoded depending on the page being viewed.

Configuration of site search on Search.gov requires an approved login to its
admin console. The [Search.gov Help Manual](https://search.gov/manual/index.html)
documents the various configuration options used on our indexes, for example
text-based "best bets" and our custom visual design.

The website base page template includes
[the necessary Search.gov code snippets](https://search.gov/manual/code.html)
required for searching and indexing of site content. Search.gov also makes use of
the website
[robots.txt](https://www.consumerfinance.gov/robots.txt)
and
[sitemap.xml](https://www.consumerfinance.gov/sitemap.xml)
files.
