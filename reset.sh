#!/bin/bash
set -euo pipefail

rsync -PhavzAX --stats --del themes/abridge/.gitignore .gitignore
rsync -PhavzAX --stats --del themes/abridge/config.toml config.toml
rsync -PhavzAX --stats --del themes/abridge/content/_index.md content/
rsync -PhavzAX --stats --del themes/abridge/COPY-TO-ROOT-SASS/* sass/
rsync -PhavzAX --stats --del themes/abridge/netlify.toml netlify.toml
rsync -PhavzAX --stats --del themes/abridge/package_abridge.js package_abridge.js
rsync -PhavzAX --stats --del themes/abridge/package.json package.json

sed -i 's/^#theme = "abridge"/theme = "abridge"/' config.toml

rsync -PhavzAX --stats --del themes/abridge/content .