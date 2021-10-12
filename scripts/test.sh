#!/bin/bash
set -euo pipefail

CHAINID=${CHAINID:-"**"}

if [[ -z ${GIT_BASE:-""} ]]; then
  CONTRACTS="contracts/$CHAINID/*json"
  PROJECTS="projects/*.json"
else
  CONTRACTS=$(git diff $GIT_BASE --name-only --diff-filter=d -- contracts/)
  PROJECTS=$(git diff $GIT_BASE --name-only --diff-filter=d -- projects/)
fi

if [[ -n $CONTRACTS ]]; then
  echo -e "Contracts:\n${CONTRACTS:0:1000}"
  echo; echo "Testing contract file names..."
  for FILE in $CONTRACTS; do
    if [[ ! $FILE =~ ^contracts/[0-9]+/0x[a-z0-9]{40}\.json$ ]]; then
      echo " Wrong filename format: $FILE"
      exit 1
    fi
  done
  echo " OK"

  echo; echo "Testing contract entries..."
  echo $CONTRACTS | xargs -n 1000 ~/go/bin/yajsv -q -s schemas/contract.json
  echo " OK"

  echo; echo "Testing project names in contract entries..."
  for PROJECT in $(echo $CONTRACTS | xargs -n 1000 jq -r '.project' | sort | uniq); do
    if [[ ! -f "projects/$PROJECT.json" ]]; then
      echo " Missing project entry: $PROJECT"
      exit 2
    fi
    echo " OK"
  done
else
  echo "No contracts to test"
fi

if [[ -n $PROJECTS ]]; then
  echo; echo -e "Projects:\n${PROJECTS:0:1000}"
  echo; echo "Testing project entries..."
  ~/go/bin/yajsv -q -s schemas/project.json $PROJECTS
  echo " OK"
else
  echo; echo "No projects to test"
fi
