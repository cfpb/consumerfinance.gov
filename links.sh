#!/bin/sh

# This script finds all the URLs in our code, as well as in elasticsearch, and
# indexes them as a type "link" which can then be queried against.


ES_HOST=localhost:9200
ES_INDEX=content
ES_DOC_TYPE=link

# Remove the existing links
curl -XDELETE $ES_HOST/$ES_INDEX/$ES_DOC_TYPE

# Create mapping
curl -XPUT $ES_HOST/$ES_INDEX/_mapping/$ES_DOC_TYPE -d '{"link":{"properties":{"url":{"type":"string"}}}}'

FILESYSTEM="$(find . -name '*.html' ! -path './src/*' ! -path './node_modules/*' ! -path './test/*' -exec cat {} \;)"
ELASTICSEARCH="$(curl -XPOST "http://$ES_HOST/$ES_INDEX/_search?format=yaml" -d '{"size" :1000000, "query": { "query_string": { "query" : "\"a href\"" } } }')"

# We need this to run some commands with sudo if on a server, but not locally
if [ "$1" = "needs_sudo" ] ; then
    echo "$FILESYSTEM$ELASTICSEARCH" \
    | perl -ne 'if (/href=\\?.https?:\/\/(?:www\.)?(?!.*gov)([^"|\/\\|\{}]*)/g) { $url = lc $1; print "{\"index\" : {\"_type\": \"'"$ES_DOC_TYPE"'\", \"_id\": \"$url\"}}\n{\"url\": \"$url\"}\n" }' | sudo tee bulk
    DELETE_CMD="sudo rm bulk"
else
    echo "$FILESYSTEM$ELASTICSEARCH" \
    | perl -ne 'if (/href=\\?.https?:\/\/(?:www\.)?(?!.*gov)([^"|\/\\|\{}]*)/g) { $url = lc $1; print "{\"index\" : {\"_type\": \"'"$ES_DOC_TYPE"'\", \"_id\": \"$url\"}}\n{\"url\": \"$url\"}\n" }' > bulk
    DELETE_CMD="rm bulk"
fi

curl -XPOST $ES_HOST/$ES_INDEX/_bulk --data-binary @bulk

$DELETE_CMD
