#!/bin/bash
OUTPUT_CSV=hypothesis.csv

echo id,user,updated,source,text,tags,html_start_node,html_end_node,start_offset,end_offset,reply_to > $OUTPUT_CSV
jq -r '{"id": .id, "user": .user, "time_update": .updated, "text": .text, "tags": .tags, "source": .target[0].source, "selector": .target[0].selector[0], "references": .references[0]} | [.id, .user, .time_update, .source, .text, (.tags | join(";")), .selector.endContainer, .selector.startContainer, .selector.startOffset, .selector.endOffset, .references] | @csv' < hypothesis.json >> $OUTPUT_CSV
