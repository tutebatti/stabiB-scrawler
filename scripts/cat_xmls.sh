#!/bin/bash

output="all_data.xml"
echo "<?xml version='1.0' encoding='UTF-8'?>" > "$output"
echo "<main>" >> "$output"

for file in ./xml_files/PPN*.mets.xml; do
    tail -n +2 "$file" >> "$output"
done

echo "</main>" >> "$output"
