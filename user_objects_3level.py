# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:20:07 2019

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
    if not os.path.exists('./user_objects/'):
        os.makedirs('./user_objects/')
except OSError:
    print ('Error: Creating directory. ' +  './user_objects/')

#insert Twitter Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

#auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

logger = logging.getLogger()
logging.basicConfig(filename="log_get_user_objects.log", format='%(message)s', filemode='w')
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





for user in followers:
    try:
        if os.path.isfile('user_objects/'+ user +'_user_objects.pickle'):
            print("Already Exists")
        else:
            us = api.get_user(user)
                
            pickle_out = open('user_objects/'+ user +'_user_objects.pickle',"wb")
            pickle.dump(us, pickle_out)
            pickle_out.close()
            
            logger.info("Completed %s" % user)
            print(user + " completed\n")
            
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue
    
for user in followings:
    try:
        if os.path.isfile('user_objects/'+ user +'_user_objects.pickle'):
            print("Already Exists")
        else:
            us = api.get_user(user)
                
            pickle_out = open('user_objects/'+ user +'_user_objects.pickle',"wb")
            pickle.dump(us, pickle_out)
            pickle_out.close()
            
            logger.info("Completed %s" % user)
            print(user + " completed\n")
            
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue    

