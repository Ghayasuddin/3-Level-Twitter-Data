# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:26:28 2019

@author: Ghayasuddin Adam
"""
import json
import glob
import logging
import tweepy
from tweepy import OAuthHandler
import os

try:
    if not os.path.exists('./lists/'):
        os.makedirs('./lists/')
except OSError:
    print ('Error: Creating directory. ' +  './lists/')

#insert Twitter Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

logger = logging.getLogger()
logging.basicConfig(filename="log_get_lists.log", format='%(message)s', filemode='w')
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


def get_all_lists(user_id):
    try:
        lis = []
        a = api.lists_memberships(user_id = user_id)
        b = api.lists_all(user_id = user_id)
        c = api.lists_subscriptions(user_id = user_id)
        d = api.lists_all(user_id = user_id, reverse = True)
        lis.extend(a)
        lis.extend(b)
        lis.extend(c)
        lis.extend(d)
        
        for l in lis:
            if os.path.isfile('lists/'+ str(l.id) +'_lists.json'):
                print("Already Exists")
            else:
                e = api.list_members(list_id = l.id)
                mem = []
                for us in e:
                    mem.append(us.id)
                
                f = api.list_subscribers(list_id = l.id)
                sub = []
                for us in f:
                    sub.append(us.id)
                
                lis_dict = {}
                lis_dict["list_id"] = l.id
                lis_dict["owner"] = l.user.id
                lis_dict["members"] = mem
                lis_dict["subscribers"] = sub
        
                with open('lists/'+ str(l.id) +'.json', 'w') as fp:
                    json.dump(lis_dict, fp, indent=2)
    except:
        print(str(user_id) + "failed")



countUser = len(followings)
for user in followings:
    countUser = countUser - 1
    try:
        get_all_lists(user)
                    
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
        get_all_lists(user)
            
        logger.info("Completed %s" % user)
        print(user + " completed userLeft(Follower) = ",end='')
        print(countUser)
                
    except:
        logger.info("Protected/Failed %s" % user)
        print(user + "Protected")
        continue
    
