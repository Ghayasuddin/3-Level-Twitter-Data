#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 4  18:14:43 2019

@author: ghayasuddin
"""


import json
import glob
import logging
import tweepy
from tweepy import OAuthHandler
import os

try:
    if not os.path.exists('./retweets/'):
        os.makedirs('./retweets/')
except OSError:
    print ('Error: Creating directory. ' +  './retweets/')

#insert Twitter Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''


auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

logger = logging.getLogger()
logging.basicConfig(filename="log_get_retweets.log", format='%(message)s', filemode='w')
logger.setLevel(logging.INFO)

tweets = []
path = 'tweets/*.json'
files = glob.glob(path)
for name in files:
    try:
        #tweets.append((os.path.splitext(os.path.basename(name))[0]))
        with open(name) as f:
            p_dict = json.load(f)
            tweets.extend([d['id'] for d in p_dict])
    except:
        continue


oldest = 0
def get_all_retweets(tweet_id):
    try:
        allretwt = []	
        uss = api.retweets(id = tweet_id,count=200,tweet_mode="extended")
        allretwt.extend(uss)
        oldest = allretwt[-1].id - 1

        while len(uss) > 0:
            print ("getting favourites before %s" % (oldest))

            uss = api.retweets(id = tweet_id,count=200,max_id=oldest)

            allretwt.extend(uss)

            oldest = allretwt[-1].id - 1
    except:
        print("No Retweets!")
        
    return allretwt

    
countTweets = len(tweets)
for twt in tweets:
    countTweets = countTweets - 1
    try:
        if os.path.isfile('retweets/'+ str(twt) +'_retweets.json'):
            print("Already Exists")
        else:
            tweets = get_all_retweets(twt)
                    
            fil = []
            for twt in tweets:
                fil.append(twt._json)
                
            with open('retweets/'+ str(twt) +'_retweets.json', 'w') as fp:
                json.dump(fil, fp, indent=2)
                    
            logger.info("Completed %s" % str(twt))
            print(str(twt) + " completed tweets left = ",end='')
            print(countTweets)
                
    except:
        logger.info("Protected/Failed %s" % str(twt))
        print(str(twt) + "Protected")
        continue


