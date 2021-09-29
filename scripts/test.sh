#!/bin/bash
set -euo pipefail

echo "Testing contract file names..."
for FILE in contracts/**/*json; do
  if [[ ! $FILE =~ ^contracts/[0-9]+/0x[A-Za-z0-9]{40}\.json$ ]]; then
    echo "Wrong filename format: $FILE"
    exit 1
  fi
done

echo; echo "Testing contract entries..."
yajsv -s schemas/contract.json contracts/**/*.json

echo; echo "Testing project entries..."
yajsv -s schemas/project.json projects/*.json

echo; echo "Success"