#!/bin/bash

# Save your personal hypothes.is developer API token to the file .hypothesis_token

HYPOTHESIS_TOKEN=$(<.hypothesis_token)
PAGE_SIZE=200
SEARCH_AFTER=""
DL_FILE="data/hypothesis.json"
# Save group ID to be searched for
FRANKEN_GROUP="7AdKKgAm"

# Build a base query that only looks within the Frankenstein Group, and then
# only within ebeshero's site
HYPOTHESIS_BASE="https://hypothes.is/api/search?sort=id&group=$FRANKEN_GROUP&uri.parts=ebeshero"

# Remove download file if it already exists
rm -f $DL_FILE

# Construct the authorization header
AUTH_HEADER="Authorization: Bearer $HYPOTHESIS_TOKEN"

# Collect total number of annotations by getting one sample search result
# and checking the `total` variable returned by hypothes.is
PING_REQUEST="$HYPOTHESIS_BASE?limit=1"
TOTAL_ANNOTATIONS=$(curl -H "$AUTH_HEADER" "$PING_REQUEST" | jq '.total')

echo "$TOTAL_ANNOTATIONS to be downloaded"

# Page through annotation downloads
for i in `seq 0 ${PAGE_SIZE} ${TOTAL_ANNOTATIONS}`;
do
  echo "$i"

  STEP_REQUEST="$HYPOTHESIS_BASE?sort=id&order=asc&search_after=$SEARCH_AFTER&limit=$PAGE_SIZE"

  echo "$STEP_REQUEST"

  # For each page of JSON results, extract the actual results and append them
  # as one line per object (using jq's -c flag) to $DL_FILE
  curl -H "$AUTH_HEADER" "$STEP_REQUEST" | jq -c ".rows[]" >> $DL_FILE

  SEARCH_AFTER=$(tail -n 1 $DL_FILE | jq -r '.id')
  jq --slurp '[.[] | .id] | unique | length' $DL_FILE
done
