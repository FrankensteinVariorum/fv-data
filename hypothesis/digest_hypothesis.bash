#!/bin/bash

jq -r '{"id": .id, "user": .user, "time_update": .updated, "text": .text, "tags": .tags, "source": .target[0].source, "selector": .target[0].selector[0]} | [.id, .user, .time_update, .source, .text, (.tags | join(";")), .selector.endContainer, .selector.startContainer, .selector.startOffset, .selector.endOffset] | @csv' < hypothesis.json > hypothesis.csv
