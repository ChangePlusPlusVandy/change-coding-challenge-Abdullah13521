# import the needed libraries
import os
import tweepy as tw
import pandas as pd
import random

# the credentials for using Twitter's API
consumer_key= 'consumer_key'
consumer_secret= 'consumer_secret'
access_token= 'access_token'
access_token_secret= 'access_token_secret'

# set up the API
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def get_all_tweets(name):
    """ function to get the past 3200 tweets made by a user """

    # start with the first 200 tweets because of the 200 limit per request
    new_tweets = api.user_timeline(screen_name = name,count=200)
    all_tweets = new_tweets

    # keep adding tweets until it reaches twitter's 3200 limit
    while len(new_tweets) > 0:

        # keep track of the oldest tweet to use in the next API request
        oldest = all_tweets[-1].id - 1
        new_tweets = api.user_timeline(screen_name = name,count=200, max_id = oldest)
        all_tweets.extend(new_tweets)

    return all_tweets

def get_texts_and_names(first_user_tweets, second_user_tweets):
    """ function to get the texts and names from the tweets and put them
    in a pandas data frame, filters the tweets that mention other users or
    include links  """

    texts = []
    names = []
    first_user_tweets.extend(second_user_tweets)

    for tweet in first_user_tweets:
        # filter the ones with links
        if "@" in tweet.text or "https" in tweet.text:
            continue

        texts.append(tweet.text)
        names.append(tweet.user.screen_name)

    return create_dataframe(texts, names)

def create_dataframe(texts, names):
    """ function to create a data frame for the tweets texts and authors columns
    """

    data = {'Tweet Text':texts, 'Tweet Author':names}
    tweets_df = pd.DataFrame(data, columns = ['Tweet Text','Tweet Author'])
    return tweets_df

def run_game(tweets_df):
    """ the main function that displays a random tweet and asks for user guess
    keeps running as long as the input is Y"""

    num_tweets = len(tweets_df)
    correct_guesses = 0
    wrong_guesses = 0

    # keep running the game as long as the input is Y
    while True:
        # pick a random tweet and display it
        n = random.randint(0, num_tweets)
        print("\n{}".format(tweets_df.iloc[n,0]))

        # get user guess
        print("\nWho wrote this tweet?")
        print("Please enter the handle of your guess: {} or {}".format(first_user, second_user))
        guess = input()

        # check if the guess is correct
        if guess == tweets_df.iloc[n,1]:
            print("\nYou guessed correctly!")
            correct_guesses += 1
        else:
            print('\nYour guess is incorrect.')
            print('Correct guess is {}'.format(tweets_df.iloc[n,1]))
            wrong_guesses += 1

        # check if user wants to continue
        print("Do you want to guess again? (Y/N)")
        reply = input()

        if reply.upper() != 'Y':
            break

    display_statistics(correct_guesses, wrong_guesses)

def display_statistics(correct_guesses, wrong_guesses):
    """ prints the game play statistics when the game is over """
    correct_percent = correct_guesses / (correct_guesses + wrong_guesses)
    print("Number of correct guesses: {}".format(correct_guesses))
    print("Percent of correct guesses: {0:.2g}".format(correct_percent))


# get the twitter handles for both users
first_user = input('Enter the twitter handle of the first user:\n')
second_user = input('\nEnter the twitter handle of the second user:\n')

# get the tweets for both users and put them in a data frame
first_user_tweets = get_all_tweets(first_user)
second_user_tweets = get_all_tweets(second_user)
tweets = get_texts_and_names(first_user_tweets, second_user_tweets)

# run the game
run_game(tweets)
