FROM blacktop/elasticsearch:7.4

# Copy Synonyms files into ElasticSearch
COPY ./cfgov/search/resources/ /usr/share/elasticsearch/config/synonyms

# Set User to Non Root
USER elasticsearch