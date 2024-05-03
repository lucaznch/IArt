#!/bin/bash

# Define color codes
RED='\033[0;31m'    # Red for fail
GREEN='\033[0;32m'  # Green for pass
NC='\033[0m'        # No color

# Iterate through each test file in the tests directory
for test_file in tests/*.txt; do
    # Extract test number from filename
    test_number=$(basename "$test_file" .txt | cut -d'-' -f2)

    # Define input, output, and result file paths
    input_file="tests/test-$test_number.txt"
    output_file="tests/test-$test_number.out"
    result_file="tests/test-$test_number.result"

    # Run pipe.py with input from the test file and save the result to a new file
    python3 pipe.py < "$input_file" > "$result_file"

    # Compare the result with the expected output
    if diff -q "$output_file" "$result_file" > /dev/null; then
        echo -e "${GREEN}Test $test_number: Passed${NC}"
    else
        echo -e "${RED}Test $test_number: Failed${NC}"
    fi
done
