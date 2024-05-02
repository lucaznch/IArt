#!/bin/bash

# Directory where the tests are located
directory="./tests"

# Counter for naming the diff files
counter=0

for txt_file in "$directory"/*.txt; do
    file_name=$(basename "$txt_file" .txt)

    out_file="$directory/$file_name.out"

    if [ -e "$out_file" ]; then
        python3 pipe.py < "$txt_file" | sed '/^\s*$/d' > temp_output.txt
        sed '/^\s*$/d' "$out_file" > temp_expected_output.txt

        if diff -q temp_output.txt temp_expected_output.txt >/dev/null; then
            echo -e "\e[32mFile $txt_file matches $out_file\e[0m"
        else
            echo -e "\e[31mFile $txt_file does not match $out_file\e[0m"
            diff temp_output.txt temp_expected_output.txt > "$directory/test-$counter.diff"
            ((counter++))
        fi

        rm temp_output.txt temp_expected_output.txt
    else
        echo -e "\e[33mFile $out_file not found.\e[0m"
    fi
done
