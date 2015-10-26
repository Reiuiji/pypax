from __future__ import absolute_import, print_function
import re
import tweepy
import configparser
from googlevoice import Voice
from googlevoice.util import input

config = configparser.ConfigParser()
config.read('twitter.cfg')
consumer_key=config.get('twitter','consumer_key')
consumer_secret=config.get('twitter','consumer_secret')
access_token=config.get('twitter','access_token')
access_token_secret=config.get('twitter','access_token_secret')
user_monitor=config.get('pypax','user_monitor')

#tweet = "It\'s the moment you\'ve all been waiting for, PAX East 2015 badges are now on sale! Get \'em while they\'re hot! http://www.showclix.com/event/3898268"
def tweetcheck(tweet):
    print(tweet)
    #find all url's
    url = re.findall(r'(https?://[^\s]+)', tweet)
    if len(url) > 0: #Found a url
        print(str(len(url)) + " Detected: " + url[0])
        sendsms(tweet)

def sendsms(message):
    voice = Voice()
    voice.login()

    phoneNumber = input('YOURNUMBER')
    text = input(str(message))

    voice.send_sms(phoneNumber, text)

class StreamListener(tweepy.StreamListener):
    ''' Handles data received from the stream. '''
 
    def on_status(self, status):
        # Find the Tweet with the mentioned tag
        if 'pax east' in status.text.lower():
            tweetcheck(status.text)
            #print(status.text)
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 
if __name__ == '__main__':
    #OAuth Connection
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    user = api.get_user(screen_name = str(user_monitor))
    print("Connected to account: " + api.me().name)
    print("Checking account to monitor: " + str(user_monitor))
    print("Account Monitor ID: " +  str(user.id))

    listener = StreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=StreamListener())
    stream.filter(follow=[str(user.id)])
#    stream.filter(track=['python'], languages=["en"])
