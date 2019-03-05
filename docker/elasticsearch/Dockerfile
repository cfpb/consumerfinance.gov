FROM elasticsearch:2.3
RUN plugin install org.codelibs/elasticsearch-dataformat/2.3.0
COPY cfgov/search/resources/synonyms_en.txt config/analysis
COPY cfgov/search/resources/synonyms_es.txt config/analysis
COPY docker/elasticsearch/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
