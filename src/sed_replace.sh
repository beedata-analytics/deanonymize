#!/bin/sh

temp_file=$(mktemp)

ESCAPED_KEYWORD=$(printf '%s\n' "\${$1}" | sed -e 's/[]\/$*.^[]/\\&/g');
ESCAPED_REPLACE=$(printf '%s\n' "$2" | sed -e 's/[\/&]/\\&/g')

# echo "$ESCAPED_KEYWORD $ESCAPED_REPLACE $3"
sed "s/$ESCAPED_KEYWORD/$ESCAPED_REPLACE/g" $3 > $temp_file && mv $temp_file $3
