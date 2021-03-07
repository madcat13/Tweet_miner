####################################
#Tweet streamer
#Streams tweets into csv file
####################################

#import libraries
import tweepy
import pandas as pd
#file extension dependency if using jupyter notebook
import import_ipynb
#import API account acccess tokens from a separate file
import access_tokens as at

#create a connection to Twitter API
auth = tweepy.OAuthHandler(at.consumer_key, at.consumer_secret)
auth.set_access_token(at.access_token, at.access_token_secret)
api = tweepy.API(auth)

#set view to  full text
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

#create a dataframe  with columns
df = pd.DataFrame(columns = ['Tweets','User_location',
                             'Tweet_date','User', 'User_ID',
                             'Tweet_ID', 'Source','User_statuses_count',
                             'User_followers', 'User_verified',
                             'Favourite_count', 'Re_tweet_count'
                            ])

#location variables for geocode with radiusses
London="51.5073219,-0.1276474,30mi"
NYC="40.7127281,-74.0060152,50mi"
Newcastle="54.966667,-1.600000,200mi"
Warwickshire="52.521757,-1.238623,140mi"


#create search parameter with search terms, exclude retweets
terms = ('coronavirus -filter:retweets OR covid-19 -filter:retweets')

#create a function to stream tweets
def stream_tweets():
    i = 0
    for tweet in tweepy.Cursor(api.search, q=terms,
                               #enter required geolocation
                               geocode= NYC,
                               #exclude replies
                               exclude_replies=True,
                               #no specific time parameters- stream most recent tweets
                               since_id=None, max_id=None,
                               #display full tweet
                               tweet_mode='extended',
                               #language parameter to English
                               lang="en",
                               #100 tweets per one request to stay within Twitter API rate limits
                               count=100).items():
        print(i, end='\r')
        #create dataframe columns
        df.loc[i, 'Tweets'] = tweet.full_text
        df.loc[i, 'User_location'] = tweet.user.location
        df.loc[i, 'Tweet_date'] = tweet.created_at
        df.loc[i, 'User'] = tweet.user.name
        df.loc[i, 'User_ID'] = tweet.user.id
        df.loc[i, 'Tweet_ID'] = tweet.id
        df.loc[i, 'Source'] = tweet.source
        df.loc[i, 'User_statuses_count'] = tweet.user.statuses_count
        df.loc[i, 'User_followers'] = tweet.user.followers_count
        df.loc[i, 'User_verified'] = tweet.user.verified
        df.loc[i, 'Favourite_count'] = tweet.favorite_count
        df.loc[i, 'Re_tweet_count'] = tweet.retweet_count
        i+=1
        #once 20k tweets is reached, break to ensure that Twitter rate limits aren't exceeded
        if i == 20000:
            break
        else:
            pass
stream_tweets()

#print first 10 records of the dataframe to visually inspect results
print(df.head(10))

#set filename path and file name
filename='/Users/username/Documents/Tweets.csv'

#save dataframe to csv, exclude index
df.to_csv(filename, index=False)
