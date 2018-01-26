"""
Scrape reddit via api

General question subredit
--------------
askreddit

More specific questions that may be useful to capture
--------------
health


https://www.reddit.com/r/AskReddit/
https://www.reddit.com/r/healthcare/
https://www.reddit.com/r/Health/

Example usage:

    python grab_reddits.py health

"""
import praw
import sys

if len(sys.argv) != 2:
    sys.exit('supply subreddit name')
subred = sys.argv[1]

# http://praw.readthedocs.io/en/latest/getting_started/quick_start.html
reddit = praw.Reddit(client_id='XXaFqoA',
                     client_secret='XXXXXXXXXXXXEePiY',
                     user_agent='general_questions')

for submission in reddit.subreddit(subred).hot(limit=10000):
    text = submission.title
    print(text.encode('ascii', 'ignore'))

for submission in reddit.subreddit(subred).new(limit=10000):
    text = submission.title
    print(text.encode('ascii', 'ignore'))
