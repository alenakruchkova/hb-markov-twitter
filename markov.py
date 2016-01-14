import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    almost_tweet = " "

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains and len(almost_tweet) <= 140:
        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)
        almost_tweet = " ".join(words)
        
    if len(almost_tweet) > 140:
        almost_tweet = " ".join(words[:-1])
        return almost_tweet
    else:
        return almost_tweet

def compare_before_posting(post):

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()


    statuses = api.GetUserTimeline("markgettysburg")
    recent_statuses = ([s.text for s in statuses])
    recent_status = recent_statuses[0]
    print "THIS IS OUR MOST RECENT STATUS : ", recent_status

    if recent_status != post:
        tweet(post)
   

def tweet(post):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    status = api.PostUpdate(post)
    print status.text

    


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

post = make_text(chains)

compare_before_posting(post)

# Your task is to write a new function tweet, that will take chains as input
# tweet(post)

