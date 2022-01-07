#!/bin/bash
up="./cfgov/unprocessed"
r="$up/js/routes"
a="$up/apps"
od="$r/on-demand"

paths=(
#header and footer
"$r/common.js"

#js for entire sub-paths
"$r/ask-cfpb/single.js"
"$r/credit-cards/single.js"
"$r/es/single.js"

#js for specific pages, based on url
"$r/about-us/careers/current-openings/index.js"
"$r/consumer-tools/debt-collection/index.js"
"$r/data-research/prepaid-accounts/search-agreements/index.js"
"$r/owning-a-home/mortgage-estimate/index.js"
"$r/owning-a-home/index.js"
"$r/external-site/index.js"

#on-demand: components included on a page via Wagtatil
#$od/*.js
"$od/simple-chart/simple-chart.js"
"$od/youth-employment-programs/buying-a-car/index.js"

#apps
$a/admin/js/*
$a/*/js/index.js
)

# command-line arguments are parsed
./node_modules/.bin/esbuild "${paths[@]}" --loader:.svg=text\
  --bundle --minify --outdir=cfgov/static_built/out "$@"
