#!/bin/bash

# Directory where the tests are located
directory="./tests"

# Counter for naming the diff files
counter=0

# Parsing command line arguments to exclude specific tests
exclude_tests=()
for arg in "$@"; do
    if [[ "$arg" == test* ]]; then
        exclude_tests+=("$arg")
    fi
done

for txt_file in "$directory"/*.txt; do
    file_name=$(basename "$txt_file" .txt)

    out_file="$directory/$file_name.out"

    if [ -e "$out_file" ]; then
        exclude=false
        for exclude_test in "${exclude_tests[@]}"; do
            if [ "$file_name" == "$exclude_test" ]; then
                exclude=true
                break
            fi
        done

        if [ "$exclude" == false ]; then
            # Using time command to get more accurate execution time
            { time python3 pipe.py < "$txt_file" | sed '/^\s*$/d' > temp_output.txt; } 2> temp_time.txt
            real_time=$(grep real temp_time.txt | awk '{print $2}')
            rm temp_time.txt

            sed '/^\s*$/d' "$out_file" > temp_expected_output.txt

            if diff -q temp_output.txt temp_expected_output.txt >/dev/null; then
                echo -e "\e[32mFile $txt_file matches $out_file\e[0m (Time taken: $real_time)"
            else
                echo -e "\e[31mFile $txt_file does not match $out_file\e[0m (Time taken: $real_time)"
                diff temp_output.txt temp_expected_output.txt > "$directory/test-$counter.diff"
                ((counter++))
            fi

            rm temp_output.txt temp_expected_output.txt
        fi
    else
        echo -e "\e[33mFile $out_file not found.\e[0m"
    fi
done
