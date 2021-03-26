FROM centos:7

# Update and install OS dependencies
RUN yum update -y && \
    yum install -y java-1.8.0-openjdk && \
    yum clean all && rm -rf /var/cache/yum

# Install ElasticSearch
RUN adduser -s /bin/false elasticsearch
RUN curl https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.5/elasticsearch-2.3.5.tar.gz -o /opt/elasticsearch.tar.gz

RUN cd /opt && \
    tar -xvf elasticsearch.tar.gz && \
    rm -rf elasticsearch.tar.gz && \
    mv elasticsearch-2.3.5 elasticsearch 

WORKDIR /opt/elasticsearch
COPY cfgov/search/resources/synonyms_en.txt config/analysis/synonyms_en.txt
COPY cfgov/search/resources/synonyms_es.txt config/analysis/synonyms_es.txt
# is this still needed?
RUN bin/plugin install org.codelibs/elasticsearch-dataformat/2.3.0

RUN chown -R elasticsearch:elasticsearch ./



EXPOSE 9200
USER elasticsearch

CMD [ "/opt/elasticsearch/bin/elasticsearch", "-Des.network.host=0.0.0.0" ]

