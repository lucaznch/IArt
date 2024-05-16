import pytest
from io import StringIO
from unittest.mock import patch
import os
import sys

# Add the path to the parent directory
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pipe

def file_tester(test_number):
    # Read the input file
    with open(f'tests/test-{test_number}.txt', 'r') as f:
        input_data = f.read().strip()
    
    # Redirect stdin and stdout
    simulated_input = StringIO(input_data)
    simulated_output = StringIO()
    
    with patch('sys.stdin', simulated_input), patch('sys.stdout', simulated_output):
        pipe.main()
    
    # Capture the generated output
    result = simulated_output.getvalue().strip()
    
    # Read the expected output file
    with open(f'tests/test-{test_number}.out', 'r') as f:
        expected_output = f.read().strip()
    
    # Compare the result with the expected output
    assert result == expected_output

@pytest.mark.parametrize("test_number", [str(i).zfill(2) for i in range(1, 10)] + ["10x10", "15x15", "20x20", "25x25", "30x30", "35x35", "40x40", "45x45", "50x50"])
@pytest.mark.timeout(200)  # Adjust timeout as needed
def test_files(test_number):
    file_tester(test_number)
