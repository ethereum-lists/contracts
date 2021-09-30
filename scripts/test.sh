#!/bin/bash
set -euo pipefail

echo "Testing contract file names..."
for FILE in contracts/**/*json; do
  if [[ ! $FILE =~ ^contracts/[0-9]+/0x[a-z0-9]{40}\.json$ ]]; then
    echo "Wrong filename format: $FILE"
    exit 1
  fi
done

echo; echo "Testing contract entries..."
echo contracts/**/*.json | xargs -n 1000 ~/go/bin/yajsv -q -s schemas/contract.json

echo; echo "Testing project entries..."
~/go/bin/yajsv -s schemas/project.json projects/*.json

echo; echo "Success"