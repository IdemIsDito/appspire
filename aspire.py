#!/usr/bin/env python

# THE SOCIAL WEB 2014 -
# FINAL ASSIGNMENT
# CREATED BY: GROUP 31
# > Jeffery Bruijntjes: #jbs257
# > Marije ten brink: #mbk262
# > Jeroen Wever: #jwr970

#imports
import re
import sys
import json
import string
import requests

from collections import Counter
# import twitter
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# #init twitter api
    # CONSUMER_KEY = 'IyGpIUZmxc3H5fZpHoKSA'
# CONSUMER_SECRET = '5ipLoZhNjh2LrUmsXvY1kiZemVqP8uUSRpCKBuTI'
# OAUTH_TOKEN = '475620020-FzXn2CzM7e31L6hzZW3tEXF5Gu5KywlzFWujVDtq'
# OAUTH_TOKEN_SECRET = 'OnMrAbIIZD2QCkj096oAiZ9WqGPOZfxiXvyCC7rw7pnmr'
# auth = twitter.oauth.OAuth(
#     OAUTH_TOKEN,
#     OAUTH_TOKEN_SECRET,
#     CONSUMER_KEY,
#     CONSUMER_SECRET)
# t = twitter.Twitter(auth=auth)

# List of all aspire words
aspireWordList = [
    'aspire','desire','want','hope','trust','request','bespeak','quest',
    'aim','plan','crave','pursue','strive','yearn','dream','hanker','long',
    'seek','try','wish','attempt','intend','plan','target','try','prefer',
    'fancy','need','choose','like'
]

# def getTweetsByScreenName(screen_name):
#     tweets = t.statuses.user_timeline(
#         screen_name=screen_name,
#         count=200,
#         include_rts=0,
#         trim_user=1
#     )
#     tweetDict = {}
#     for tweet in tweets:
#         tweetDict[tweet['id']] = tweet['text'].encode("utf-8")
#     return tweetDict

def getTweetsFromGrepTweet(screen_name):
    # uses greptweet
    # http://docs.python-requests.org/en/latest/api/
    fetchurl='http://greptweet.com/f/%s'
    grepcontenturl ='http://greptweet.com/u/%s/tweets.txt'
    requests.get(fetchurl % (screen_name))
    tweets_raw = requests.get(grepcontenturl % (screen_name))
    tweetDict = {}
    for text in tweets_raw.iter_lines():
        tweet = text.split('|')
        tweetDict[tweet[0]] = tweet[-1]
    return tweetDict

def cleanTweets(tweetDict):
    filteredDict = {}
    for tweetId, tweetText in tweetDict.iteritems():
        tweetText = tweetText.lower()
        # remove RT
        tweetText = re.sub(r'\brt\b', '', tweetText)
        # remove links
        tweetText = re.sub(r'(http://|www.)(.*)\b', '', tweetText)
        # remove hashtags
        tweetText = re.sub(r'#(.*)\b', '', tweetText)
        # remove mentions
        tweetText = re.sub(r'@(.*)\b', '', tweetText)
        # remove punctuation
        no_punct = tweetText.translate(None, string.punctuation)
        # tokenize
        tokens = nltk.word_tokenize(no_punct)
        # remove stopwords
        wordList = [w for w in tokens if not w in stopwords.words('english')]

        filteredDict[tweetId] = wordList
    return filteredDict

def createAspireWordList():
    # http://docs.python-requests.org/en/latest/api/
    baseWords = [
        'aspire','desire','hope','trust','wish','dream'
    ]
    APIKEY = 'f9f7cb2450e798a4a27274815d7c1199'
    apiurl='http://words.bighugelabs.com/api/2/%s/%s/'
    wordList = []
    for w in baseWords:
        words = requests.get(apiurl % (APIKEY, w))
        for text in words.iter_lines():
            tweet = text.split('|')
            if tweet[0] == 'verb' and tweet[1] == 'syn':
                wordList.append(tweet[2])
    return wordList

def extractAspirationalTweets(tweetDict):
    aspireWordList = createAspireWordList();
    print len(aspireWordList)
    extractedDict = {}
    for tweetId, tweetWords in tweetDict.iteritems():
        for w in tweetWords:
            if w in aspireWordList:
                tweetWords.remove(w)
                extractedDict[tweetId] = tweetWords
    return extractedDict

def countWords(tweetDict):
    tweetWordFreqDict = {}
    for tweetId, tweetWordList in tweetDict.iteritems():
        for word in tweetWordList:
            if word in tweetWordFreqDict:
                tweetWordFreqDict[word]+=1
            else:
                tweetWordFreqDict[word]=1
    d = Counter(tweetWordFreqDict)
    returnDict = {}
    for key, value in d.most_common(25):
        returnDict[key] = value
    return returnDict

def stemTweets(tweets):
    stemmer = PorterStemmer()
    for tweetId, tweetWordList in tweets.iteritems():
        for index, word in enumerate(tweetWordList):
            tweetWordList[index] = stemmer.stem(word)
    return tweets

def start(screen_name):
    tweets = getTweetsFromGrepTweet(screen_name)
    cleanedTweets = cleanTweets(tweets)
    extractedTweets = extractAspirationalTweets(cleanedTweets)
    stemmedTweets = stemTweets(extractedTweets)
    return countWords(stemmedTweets)

# Main
if __name__ == '__main__':
    screen_name = sys.argv[1].lower()
    print json.dumps(start(screen_name), indent=4)