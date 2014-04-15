#!/usr/bin/env python

import tweepy
import json
import sys
import ConfigParser as cfg


# Authentication details. To  obtain these visit dev.twitter.com
config = cfg.ConfigParser()
config.read('twitter.conf')
consumer_key = config.get(sys.argv[2], 'consumer_key')
consumer_secret = config.get(sys.argv[2], 'consumer_secret')
access_token = config.get(sys.argv[2], 'access_token')
access_token_secret = config.get(sys.argv[2], 'access_token_secret')




# This is the listener, resposible for receiving data

class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):

        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        if decoded.has_key('user'):
            print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        elif decoded.has_key('text'):
            print '%s' % (decoded['text'].encode('ascii', 'ignore'))
        else:
            print data
        
        return True


    def on_error(self, status):
        print status



if __name__ == '__main__':

    l = StdOutListener()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)



    print "Showing all new tweets for #:" , sys.argv[1]



    # There are different kinds of streams: public stream, user stream, multi-user streams

    # In this example follow #http tag

    # For more details refer to https://dev.twitter.com/docs/streaming-apis

    stream = tweepy.Stream(auth, l)

    stream.filter(track=[sys.argv[1]])
