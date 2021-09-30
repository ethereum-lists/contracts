#!/bin/bash
set -euo pipefail

CHAINID="**"

echo "Testing contract file names..."
for FILE in contracts/$CHAINID/*json; do
  if [[ ! $FILE =~ ^contracts/[0-9]+/0x[a-z0-9]{40}\.json$ ]]; then
    echo " Wrong filename format: $FILE"
    exit 1
  fi
done
echo " OK"

echo; echo "Testing contract entries..."
echo contracts/$CHAINID/*.json | xargs -n 1000 ~/go/bin/yajsv -q -s schemas/contract.json
echo " OK"

echo; echo "Testing project entries..."
~/go/bin/yajsv -q -s schemas/project.json projects/*.json
echo " OK"

echo; echo "Testing project names in contract entries..."
for PROJECT in $(echo contracts/$CHAINID/*.json | xargs -n 1000 jq -r '.project' | sort | uniq); do
  if [[ ! -f "projects/$PROJECT.json" ]]; then
    echo " Missing project entry: $PROJECT"
    exit 2
  fi
done

echo " OK"
