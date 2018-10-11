#!/bin/bash

# Save your personal hypothes.is developer API token to the file .hypothesis_token

HYPOTHESIS_TOKEN=$(<.hypothesis_token)
PAGE_SIZE=200
HYPOTHESIS_BASE="https://hypothes.is/api/search"
DL_FILE="hypothesis.json"

# Save group ID to be searched for
FRANKEN_GROUP="GwWrAWaw"

# Remove download file if it already exists
rm -f $DL_FILE

# Construct the authorization header
AUTH_HEADER="Authorization: Bearer $HYPOTHESIS_TOKEN"

# Collect total number of annotations
PING_REQUEST="$HYPOTHESIS_BASE?limit=1&group=$FRANKEN_GROUP&sort=id"
TOTAL_ANNOTATIONS=$(curl -H "$AUTH_HEADER" "$PING_REQUEST" | jq '.total')

echo "$TOTAL_ANNOTATIONS to be downloaded"

# Page through annotation downloads
for i in `seq 0 ${PAGE_SIZE} ${TOTAL_ANNOTATIONS}`;
do
  echo "$i"

  STEP_REQUEST="$HYPOTHESIS_BASE?offset=$i&limit=$PAGE_SIZE&group=$FRANKEN_GROUP&sort=id"

  echo "$STEP_REQUEST"

  # For each page of JSON results, extract the actual results and append them
  # as one line per object (using jq's -c flag) to $DL_FILE
  curl -H "$AUTH_HEADER" "$STEP_REQUEST" | jq -c ".rows[]" >> $DL_FILE
done
