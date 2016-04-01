# InsightTwitterProject
Insight Data Engineering - Coding Challenge https://github.com/InsightDataScience/coding-challenge

Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. You will thus be calculating the average degree over a 60-second sliding window. 

## Tests
python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/output.txt

input file "tweets.txt" contains tweet lines in JSON format. This file can be obtained through Twitter's API in JSON format.

output file "output.txt" gives the average degree of a vertex in a Twitter hashtag graph within the last 60 seconds.
