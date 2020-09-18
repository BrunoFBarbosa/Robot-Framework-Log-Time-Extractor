# Robot Framework Log Time Extractor
A simple tool to extract the execution time for keywords, suites and test cases from robot framework logs.
This script was created in order to get an overview of what tests/keywords/suites are taking longer to be executed, helping to visualize the best candidates for a refactor and understand where is the bottleneck of a test suite.

# How it works

It works by simply parsing the output.xml generated from Robot Framework and generate 3 CSVs files containing how much time it took for the tests, suites and also keywords to run. This script also maps how many times a keyword is used, how many test cases are there in a suite and its average duration

# Usage

1. Create a folder called "runs" on the same directory of this script
2. Put all the output.xml files you want inside of it
3. Simply run:
```
python run_parser.py
```

This will generate a "results" folder with the 3 CSVs files mentioned above

# Output Example:

## Keywords
<img src="/images/keyword_example.PNG" alt="Keywords generated file example"/>


## Tests Cases
<img src="/images/test_example.PNG" alt="Tests generated file example"/>


## Suites
<img src="/images/suite_example.PNG" alt="Suites generated file example"/>
