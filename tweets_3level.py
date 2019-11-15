# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:22:15 2019

@author: Ghayasuddin Adam
"""

# importing libraries
import json
import glob
import pickle
import logging
import tweepy
from tweepy import OAuthHandler
import os

try:
    if not os.path.exists('./tweets/'):
        os.makedirs('./tweets/')
except OSError:
    print ('Error: Creating directory. ' +  './tweets/')
    
#insert Twitter Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''            

#auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

logger = logging.getLogger()
logging.basicConfig(filename="log_get_tweets.log", format='%(message)s', filemode='w')
logger.setLevel(logging.INFO)

followings = []
path = 'followings/*.json'
files = glob.glob(path)
for name in files:
    try:
        followings.append((os.path.splitext(os.path.basename(name))[0]))
        with open(name) as f:
            p_dict = json.load(f)
            followings.extend(p_dict)
    except:
        continue
    
followers = []
path = 'followers/*.json'
files = glob.glob(path)
for name in files:
    try:
        followers.append((os.path.splitext(os.path.basename(name))[0]))
        with open(name) as f:
            p_dict = json.load(f)
            followers.extend(p_dict)
    except:
        continue


oldest = 0
def get_all_tweets(user_id):
	#Twitter only allows most recent 3240 tweets using user timeline method
    alltweets = []
    new_tweets = api.user_timeline(id = user_id,count=200)
    alltweets.extend(new_tweets)
    	
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    i = 0
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(id = user_id,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        i = i + 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))
	
    return alltweets


for user in followings:
    try:
        if os.path.isfile('tweets/'+ user +'_tweets.pickle'):
            print("Already Exists")
        else:
            tweets = get_all_tweets(user)
                
            pickle_out = open('tweets/'+ user +'_tweets.pickle',"wb")
            pickle.dump(tweets, pickle_out)
            pickle_out.close()
                
            logger.info("Completed %s" % user)
            print(user + " completed\n")
                
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue
    
    
for user in followers:
    try:
        if os.path.isfile('tweets/'+ user +'_tweets.pickle'):
            print("Already Exists")
        else:
            tweets = get_all_tweets(user)
                
            pickle_out = open('tweets/'+ user +'_tweets.pickle',"wb")
            pickle.dump(tweets, pickle_out)
            pickle_out.close()
                
            logger.info("Completed %s" % user)
            print(user + " completed\n")
                
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue

