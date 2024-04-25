#!/bin/bash

# Directory where the tests are located
directory="./tests"

for txt_file in "$directory"/*.txt; do
    file_name=$(basename "$txt_file" .txt)

    out_file="$directory/$file_name.out"

    if [ -e "$out_file" ]; then
        python3 pipe.py < "$txt_file" > temp_output.txt

        if diff -q temp_output.txt "$out_file" >/dev/null; then
            echo -e "\e[32mFile $txt_file matches $out_file\e[0m"
        else
            echo -e "\e[31mFile $txt_file does not match $out_file\e[0m"
        fi

        rm temp_output.txt
    else
        echo -e "\e[33mFile $out_file not found.\e[0m"
    fi
done
