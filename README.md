# twitter_test


pip install -r requirements.txt - to download all packages needed to work with twitter_test

1. TweetParser in parser_func.py:
*   TweetParser.fetch_user - can get all general information from tweet user(use save_user(data) - to save all parsed info to mysql db).
*   TweetParser.fetch - can get approximately 3200-3250 tweets is max for parsing from each user(use save_tweet_data(account) - to save tweets you've collected to db).

2. db_func.py:
 I put all functions related to work with the db here. 
