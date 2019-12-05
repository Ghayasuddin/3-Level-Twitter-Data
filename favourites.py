# -*- coding: utf-8 -*-
"""
Created on Thu May  2 23:09:38 2019

@author: Ghayasuddin Adam
"""

import json
import glob
import logging
import tweepy
from tweepy import OAuthHandler
import os

try:
    if not os.path.exists('./favorites/'):
        os.makedirs('./favorites/')
except OSError:
    print ('Error: Creating directory. ' +  './favorites/')

#insert Twitter Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''


auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

logger = logging.getLogger()
logging.basicConfig(filename="log_get_favorites.log", format='%(message)s', filemode='w')
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
def get_all_favtweets(user_id):
    allfav = []	
    uss = api.favorites(id = user_id,count=200,tweet_mode="extended")
    allfav.extend(uss)
    oldest = allfav[-1].id - 1
    
    while len(uss) > 0:
        print ("getting favourites before %s" % (oldest))
        		
        uss = api.favorites(id = user_id,count=200,max_id=oldest)
        		
        allfav.extend(uss)
        
        oldest = allfav[-1].id - 1
        
    return allfav


countUser = len(followings)
for user in followings:
    countUser = countUser - 1
    try:
        if os.path.isfile('favorites/'+ user +'_favorites.json'):
            print("Already Exists")
        else:
            tweets = get_all_favtweets(user) 
            fil = []
            for twt in tweets:
                fil.append(twt._json)
                
            with open('favorites/'+ user +'_favorites.json', 'w') as fp:
                json.dump(fil, fp, indent=2)
                    
            logger.info("Completed %s" % user)
            print(user + " completed userLeft(Following) = ",end='')
            print(countUser)
				
                
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue
    
    
countUser = len(followers)
for user in followers:
    countUser = countUser - 1
    try:
        if os.path.isfile('favorites/'+ user +'_favorites.json'):
            print("Already Exists")
        else:
            tweets = get_all_favtweets(user)
                    
            fil = []
            for twt in tweets:
                fil.append(twt._json)
                
            with open('favorites/'+ user +'_favorites.json', 'w') as fp:
                json.dump(fil, fp, indent=2)
                    
            logger.info("Completed %s" % user)
            print(user + " completed userLeft(Follower) = ",end='')
            print(countUser)
                
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue
    
