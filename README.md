# Robot Framework Log Time Extractor
A simple tool to extract the execution time for keywords, suites and test cases from robot framework logs
This script was created in order to get an idea of what tests are taking more time to be executed and therefore becoming candidates for a refactor. 

# How it works

It simply works by parsing the output.xml generated from Robot Framework and generate 3 CSVs files containing how much time it took for the tests, suites and also keywords to run

Ex:

