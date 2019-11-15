# 3-Level-Twitter-Data
Get three level twitter data from tweet id 

	First Get your keys from twitter

<b>Imports:</b>

	tweepy
	
<b>Process:</b>
	
	First step:
		Get tweet ids of tweet in a text file named tweet_ids.txt
		
	Second step:
		Run followers_3level.py and followings_3level.py to collect 3 degree friends and followers of users involved in tweets
		This include mentioned, author of tweet, if tweet is a reply then it also add user of tweet which is replied to.
		
		Output files are saved in followers and followings folder
		username is filename and format is json
		
		Note: it contains ids of users only
		
	Third step:
		Run tweets_3level.py and user_objects_3level.py to collect user object and tweet object of collected users 
		
		Output files are saved in tweets and user_objects folder
		username is filename and format is pickle


