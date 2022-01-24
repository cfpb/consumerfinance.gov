set -e

DROP_PREAMBLE=$(cat << EOF
  SET client_min_messages = WARNING;
  DROP SCHEMA IF EXISTS cfpb CASCADE;
EOF
)

(echo "$DROP_PREAMBLE" && pg_dump --no-owner --no-privileges --user=cfpb postgres://cfpb:cfpb@postgres/cfgov) | gzip > test.sql.gz
