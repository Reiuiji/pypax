from __future__ import absolute_import, print_function

import tweepy
import ConfigParser

#Config Setup
config = ConfigParser.ConfigParser()
config.read('twitter.cfg')
consumer_key=config.get('twitter','consumer_key')
consumer_secret=config.get('twitter','consumer_secret')
access_token=config.get('twitter','access_token')
access_token_secret=config.get('twitter','access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)

#api.update_status(status='Going to do some twitter testing right now')

api.update_status(status='Testing!!! It\'s the moment you\'ve all been waiting for, PAX East 2015 badges are now on sale! Get \'em while they\'re hot! [link]')

