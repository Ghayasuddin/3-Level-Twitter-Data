# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:21:56 2019

@author: Ghayasuddin Adam
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:21:36 2019

@author: Ghayasuddin Adam
"""

# importing libraries
import json
import logging
import tweepy
from tweepy import OAuthHandler
import os
import time

try:
    if not os.path.exists('./followings/'):
        os.makedirs('./followings/')
except OSError:
    print ('Error: Creating directory. ' +  './followings/')

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
logging.basicConfig(filename="log_get_followings.log", format='%(message)s', filemode='w')
logger.setLevel(logging.INFO)

#Reading Main Users
f = open('tweet_ids.txt', 'r')
tweet_id_list = f.readlines()
f.close()
tweet_id_list = [item.rstrip() for item in tweet_id_list]

level1_users = []
for id in tweet_id_list:
    try:
        users_list = []
        tweet = api.get_status(id)
        users_list.append(tweet.user.id_str)
        if tweet.in_reply_to_user_id_str is not None:
            users_list.append(tweet.in_reply_to_user_id_str)
        if tweet.entities["user_mentions"] is not None:
            for u in tweet.entities["user_mentions"]:
                users_list.append(u["id_str"])
        for user in users_list:
            try:
                if os.path.isfile('followings/'+ user +'_followings.json'):
                    print("Already Exists")
                else:
                    friends_ids = []
                    for page in tweepy.Cursor(api.friends_ids,stringify_ids = True, user_id = user).pages():
                        friends_ids.extend(page)
                        time.sleep(60)
                
                    with open('followings/'+ user +'_followings.json', 'w') as write_file:
                        json.dump(friends_ids, write_file)
                    
					level1_users.append(friends_ids)
                    logger.info("Completed %s" % user)
                    print(user + " completed\n")
                
            except:
                logger.info("Protected/Failed %s" % user)
                print(user + "Protected")
                continue
        logger.info("Completed tweet %s" % id)
        print(id + " tweet completed\n")
    except:
        continue
		

friends_ids = []

print("Level 2\n")
logger.info("LEVEL 2")
level2_users = []
for user in level1_users:
    try:
		if os.path.isfile('followings/'+ user +'_followings.json'):
			print("Already Exists")
		else:
            friends_ids = []
			for page in tweepy.Cursor(api.friends_ids,stringify_ids = True, user_id = user).pages():
				friends_ids.extend(page)
                time.sleep(60)
                
            with open('followings/'+ user +'_followings.json', 'w') as write_file:
                json.dump(friends_ids, write_file)
                    
			level2_users.append(friends_ids)
            logger.info("Completed %s" % user)
            print(user + " completed\n")
                
    except:
		logger.info("Protected/Failed %s" % user)
		print(user + "Protected")
		continue

print("\nSaved level 2 followings ids.....")

friends_ids = []

print("Level 3\n")
logger.info("LEVEL 3")
for user in level2_users:
    try:
		if os.path.isfile('followings/'+ user +'_followings.json'):
			print("Already Exists")
		else:
            friends_ids = []
			for page in tweepy.Cursor(api.friends_ids,stringify_ids = True, user_id = user).pages():
				friends_ids.extend(page)
                time.sleep(60)
                
            with open('followings/'+ user +'_followings.json', 'w') as write_file:
                json.dump(friends_ids, write_file)
                
            logger.info("Completed %s" % user)
            print(user + " completed\n")
                
    except:
		logger.info("Protected/Failed %s" % user)
		print(user + "Protected")
		continue

print("\nSaved level 3 followings ids.....")